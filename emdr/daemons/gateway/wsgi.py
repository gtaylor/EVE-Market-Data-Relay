"""
This WSGI application accepts market data uploads from various uploader clients.
The various URLs below are structured to pass off the parsing based on what
format the data is in.

Once parsed, the data is shoved out to the Announcers via the
gateway.order_pusher module.
"""
# Logging has to be configured first before we do anything.
import logging
import urllib
import zlib

logger = logging.getLogger(__name__)

import gevent
#noinspection PyUnresolvedReferences
from bottle import run, request, response, post, default_app

from emdr.daemons.gateway import order_pusher
from emdr.daemons.gateway.exceptions import MalformedUploadError
from emdr.core.serialization.exceptions import InvalidMarketOrderDataError
from emdr.core.serialization import unified
from emdr.core.serialization import eve_marketeer

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

    if content_encoding == 'gzip' or content_encoding == 'deflate':
        # Compressed request
        try:
            # Auto header checking.
            message_body = zlib.decompress(message_body, 15 + 32)
        except zlib.error:
            # Negative wbits suppresses adler32 checksumming.
            message_body = zlib.decompress(message_body, -15)
        # Url decode the body
        message_body = urllib.unquote_plus(message_body)
        if message_body[:5] == 'data=':
            message_body = message_body[5:]
    else:
        # Uncompressed request
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
    except (InvalidMarketOrderDataError, MalformedUploadError) as exc:
        # Something bad happened. We know this will return at least a
        # semi-useful error message, so do so.
        response.status = 400
        logger.error("Error to %s: %s" % (get_remote_address(), exc.message))
        return exc.message

    # Sends the parsed MarketOrderList or MarketHistoryList to the Announcers
    # as compressed JSON.
    gevent.spawn(order_pusher.push_message, parsed_message)

    logger.info("Accepted %s %s upload from %s" % (
        upload_format, parsed_message.result_type, get_remote_address()
    ))
    # Goofy, but apparently expected by EVE Market Data Uploader.
    return '1'

@post('/upload/eve_marketeer/')
def upload_eve_marketeer():
    """
    This view accepts uploads in EVE Marketeer or EVE Marketdata format. These
    typically arrive via the EVE Unified Uploader client.
    """
    if request.forms.log.startswith('none'):
        logger.error('Rejecting empty EMK order or history list.')
        # EVE Marketeer Uploader uploads an empty entry when a given item isn't
        # available in the player's filtered area. This typically happens when
        # market scanners point them there. We'll just not our head and go
        # along for now.
        return '1'

    # Message dicts are a way to package/wrap uploaded data in a way that lets
    # the processor nodes know what format the upload is in. The payload attrib
    # contains the format-specific stuff.
    message_dict = {
        'format': 'eve_marketeer',
        'remote_address': get_remote_address(),
        'payload': {
            # 'orders' or 'history'
            'upload_type': request.forms.upload_type,
            'type_id': request.forms.type_id,
            'region_id': request.forms.region_id,
            # CSV, with \r\n delimited records.
            'log': request.forms.log,
            # 'EVEUnifiedUploader'
            'developer_key': request.forms.developer_key,
            # String, like '6.0'
            'version': request.forms.version,
            # 2012-03-11 01:24:33
            'generated_at': request.forms.generated_at,
            # Upload key, arbitrary
            'upload_key': request.forms.upload_key,
        }
    }

    return parse_and_error_handle(
        eve_marketeer.parse_from_payload, message_dict['payload'], 'EMK'
    )

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

    return parse_and_error_handle(
        unified.parse_from_json, message_body, 'Unified'
    )

@post('/upload/')
def upload():
    """
    Convenience URL that determines what format the upload is coming in,
    then routes to the correct logic for said format.
    """
    if request.forms.upload_key and request.forms.developer_key:
        # EVE Marketeer has these two form values.
        return upload_eve_marketeer()
    else:
        # Since Unified format is a straight POST with a body, we'll naively
        # assume anything else is the Unified format. Note that improperly
        # formed uploads that have no POST keys will be caught by this, and
        # a JSON error will be shown. This may confuse some users.
        return upload_unified()
