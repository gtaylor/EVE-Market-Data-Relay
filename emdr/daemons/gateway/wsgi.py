"""
This WSGI application accepts market data uploads from various uploader clients.
The various URLs below are structured to pass off the parsing based on what
format the data is in.

The order data is re-packaged, then sent off to the processor nodes,
where the data is parsed, some light validation is performed, then passed off
to the relay for re-broadcasting to consumers.
"""
# Logging has to be configured first before we do anything.
import logging
from logging.config import dictConfig
import zlib
from emdr.conf import default_settings as settings
dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

import gevent
from gevent import monkey; gevent.monkey.patch_all()
#noinspection PyUnresolvedReferences
from bottle import run, request, response, post, default_app

from emdr.daemons.gateway import order_pusher

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
    if request.headers.get('Content-Encoding', '') == 'gzip':
        # Negative wbits supresses adler32 checksumming.
        return zlib.decompress(request.body.read(), wbits=-15)
    else:
        return request.body.read()

@post('/upload/eve_marketeer/')
def upload_eve_marketeer():
    """
    This view accepts uploads in EVE Marketeer or EVE Marketdata format. These
    typically arrive via the EVE Unified Uploader client.
    """
    # Message dicts are a way to package/wrap uploaded data in a way that lets
    # the processor nodes know what format the upload is in. The payload attrib
    # contains the format-specific stuff.
    if request.forms.log.startswith('none'):
        # Unified Uploader uploads an empty entry when a given item isn't
        # available in the player's filtered area. This typically happens when
        # market scanners point them there. We'll just not our hend and go
        # along for now.
        return '1'

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

    # Some very basic sanity checking.
    for key, value in message_dict['payload'].items():
        if not value:
            response.status = 400
            logger.error('In EMK POST from %s, missing key: %s' % (
                get_remote_address(), key))
            return 'No value specified for key: %s' % key

    # The message dict gets shoved into a gevent queue, where it awaits sending
    # to the processors via the src.daemons.gateway.order_pusher module.
    order_pusher.order_upload_queue.put(message_dict)
    logger.info("Accepted EMK upload from %s" % get_remote_address())

    # Goofy, but apparently expected by EVE Market Data Uploader.
    return '1'

@post('/upload/unified/')
def upload_unified():
    """
    This view accepts uploads in Unified Uploader format. These
    typically arrive via the EVE Unified Uploader client.
    """
    message_dict = {
        'format': 'unified',
        'remote_address': get_remote_address(),
        'payload': {
            # The HTTP request's body can be gzip'd, so de-compress and return
            # it if the gzip Content-Encoding is detected.
            'body': get_decompressed_message(),
        }
    }

    # The message dict gets shoved into a gevent queue, where it awaits sending
    # to the processors via the src.daemons.gateway.order_pusher module.
    order_pusher.order_upload_queue.put(message_dict)
    logger.info("Accepted Unified upload from %s" % get_remote_address())

    # Goofy, but apparently expected by EVE Market Data Uploader.
    return 'OK'

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
        # assume anything else is the Unified format.
        return upload_unified()
