"""
This WSGI application accepts market data uploads from various uploader clients.
The various URLs below are structured to pass off the parsing based on what
format the data is in.

Once parsed, the data is shoved out to the Announcers via the
gateway.order_pusher module.
"""
# Logging has to be configured first before we do anything.
import logging
import urlparse
import zlib

logger = logging.getLogger(__name__)

import gevent
#noinspection PyUnresolvedReferences
from bottle import run, request, response, get, post, default_app

from emds.formats import unified
from emds.formats.exceptions import ParseError
from emdr import __version__ as EMDR_VERSION
from emdr.daemons.gateway import order_pusher
from emdr.daemons.gateway.exceptions import MalformedUploadError
from emds.exceptions import EMDSError

def get_remote_address():
    """
    Determines the address of the uploading client. First checks the for
    proxy-forwarded headers, then falls back to request.remote_addr.

    :rtype: str
    """
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def get_decompressed_message():
    """
    For upload formats that support it, detect gzip Content-Encoding headers
    and de-compress on the fly.

    :rtype: str
    :returns: The de-compressed request body.
    """
    content_encoding = request.headers.get('Content-Encoding', '')

    if content_encoding in ['gzip', 'deflate']:
        # Compressed request. We have to decompress the body, then figure out
        # if it's form-encoded.
        try:
            # Auto header checking.
            message_body = zlib.decompress(request.body.read(), 15 + 32)
        except zlib.error:
            # Negative wbits suppresses adler32 checksumming.
            message_body = zlib.decompress(request.body.read(), -15)

        # At this point, we're not sure whether we're dealing with a straight
        # un-encoded POST body, or a form-encoded POST. Attempt to parse the
        # body. If it's not form-encoded, this will return an empty dict.
        form_enc_parsed = urlparse.parse_qs(message_body)
        if form_enc_parsed:
            # This is a form-encoded POST. The value of the data attrib will
            # be the body we're looking for.
            try:
                message_body = form_enc_parsed['data'][0]
            except (KeyError, IndexError):
                raise MalformedUploadError(
                    "No 'data' POST key/value found. Check your POST key "
                    "name for spelling, and make sure you're passing a value."
                )
    else:
        # Uncompressed request. Bottle handles all of the parsing of the
        # POST key/vals, or un-encoded body.
        data_key = request.forms.get('data')
        if data_key:
            # This is a form-encoded POST. Support the silly people.
            message_body = data_key
        else:
            # This is a non form-encoded POST body.
            message_body = request.body.read()

    return message_body

def parse_and_error_handle(parser, data, upload_format):
    """
    Standardized parsing and error handling for parsing. Returns the final
    HTTP body to send back to the uploader after parsing, or error messages.

    :param callable parser: The parser function to use to parse ``data``.
    :param object data: An dict or str of parser-specific data to parse
        using the callable specified in ``parser``.
    :param str upload_format: Upload format identifier for the logs.
    :rtype: str
    :returns: The HTTP body to return.
    """
    try:
        parsed_message = parser(data)
    except (
        EMDSError, MalformedUploadError, TypeError, ValueError
    ) as exc:
        # Something bad happened. We know this will return at least a
        # semi-useful error message, so do so.
        response.status = 400
        logger.error("Error to %s: %s" % (get_remote_address(), exc.message))
        return exc.message

    # Sends the parsed MarketOrderList or MarketHistoryList to the Announcers
    # as compressed JSON.
    gevent.spawn(order_pusher.push_message, parsed_message)

    logger.info("Accepted %s %s upload from %s" % (
        upload_format, parsed_message.list_type, get_remote_address()
    ))
    # Goofy, but apparently expected by EVE Market Data Uploader.
    return '1'

@post('/upload/unified/')
def upload_unified():
    """
    This view accepts uploads in Unified Uploader format. These
    typically arrive via the EVE Unified Uploader client.
    """
    try:
        # Body may or may not be compressed.
        message_body = get_decompressed_message()
    except zlib.error as exc:
        # Some languages and libs do a crap job zlib compressing stuff. Provide
        # at least some kind of feedback for them to try to get pointed in
        # the correct direction.
        response.status = 400
        # I'm curious how common this is, keep an eye out.
        logger.error("gzip error with %s: %s" % (get_remote_address(), exc.message))
        return exc.message
    except MalformedUploadError as exc:
        # They probably sent an encoded POST, but got the key/val wrong.
        response.status = 400
        logger.error("Error to %s: %s" % (get_remote_address(), exc.message))
        return exc.message


    return parse_and_error_handle(
        unified.parse_from_json, message_body, 'Unified'
    )

@post('/upload/')
def upload():
    """
    Convenience URL that determines what format the upload is coming in,
    then routes to the correct logic for said format.
    """
    # We only support UUDIF for now.
    return upload_unified()

@get('/health_check/')
def health_check():
    """
    This should only be used by the gateway monitoring script. It is used
    to detect whether the gateway is still alive, and whether it should remain
    in the DNS rotation.
    """
    return EMDR_VERSION