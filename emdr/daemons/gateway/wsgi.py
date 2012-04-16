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
from emdr.conf import default_settings as settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('emdr.daemons.gateway.wsgi')

import gevent
from gevent import monkey; gevent.monkey.patch_all()
#noinspection PyUnresolvedReferences
from bottle import run, request, post, default_app

from emdr.daemons.gateway import order_pusher

@post('/upload/eve_marketeer/')
def upload_eve_marketeer():
    """
    This view accepts uploads in EVE Marketeer or EVE Marketdata format. These
    typically arrive via the EVE Unified Uploader client.
    """
    # Job dicts are a way to package/wrap uploaded data in a way that lets
    # the processor nodes know what format the upload is in. The payload attrib
    # contains the format-specific stuff.
    #print "TEST", request.forms.keys()
    #print "TEST", request.forms.items()
    job_dict = {
        'format': 'eve_marketeer',
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
        }
    }

    # The job dict gets shoved into a gevent queue, where it awaits sending
    # to the processors via the src.daemons.gateway.order_pusher module.
    order_pusher.order_upload_queue.put(job_dict)
    logger.info("Accepted upload from %s" % request.remote_addr)

    # Goofy, but apparently expected by EVE Market Data Uploader.
    return '1'

@post('/upload/unified/')
def upload_eve_marketeer():
    """
    This view accepts uploads in Unified Uploader format. These
    typically arrive via the EVE Unified Uploader client.
    """
    job_dict = {
        'format': 'unified',
        'payload': {
            'body': request.body.read(),
        }
    }

    # The job dict gets shoved into a gevent queue, where it awaits sending
    # to the processors via the src.daemons.gateway.order_pusher module.
    order_pusher.order_upload_queue.put(job_dict)
    logger.info("Accepted upload from %s" % request.remote_addr)

    # Goofy, but apparently expected by EVE Market Data Uploader.
    return '1'
