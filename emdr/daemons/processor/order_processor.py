"""
The worker function in this module performs the order and history processing.
"""
import logging
import zlib
import simplejson
from simplejson.decoder import JSONDecodeError
from emdr.core.serialization import unified
from emdr.core.serialization import eve_marketeer

logger = logging.getLogger(__name__)

def parse_message(job_json):
    """
    Routes the order or history message to the correct parser, returns the
    parsed order or history in Unified Uploader format.

    :param str job_json: A raw JSON job dict string to parse.
    :rtype: MarketOrderList or MarketHistory
    :returns: A serializable MarketOrderList or MarketHistory instance.
    """
    job_dict = simplejson.loads(zlib.decompress(job_json))

    # The remote address who sent the message. This can be spoofed.
    remote_ip = job_dict['remote_address']
    # The format attrib on the job dict determines which parser to use.
    message_format = job_dict.get('format', 'unknown')

    try:
        # A payload must exist, regardless of the format. The payload contains
        # the data passed to the gateway.
        payload = job_dict['payload']
    except KeyError:
        logger.error('Job from %s dict has no payload key. Discarding.' % remote_ip)
        return

    if message_format == 'unified':
        try:
            message = unified.parse_from_json(payload['body'])
        except JSONDecodeError:
            # Probably an uploader uploading to the wrong endpoint.
            logger.error('JSON decoding error encountered in message from %s. Discarding.' % remote_ip)
            return
    elif message_format == 'eve_marketeer':
        message = eve_marketeer.parse_from_payload(payload)
    else:
        logger.error('Unknown message format encountered in message from %s. Discarding.' % remote_ip)
        return

    logger.info('Message from %s processed and relayed.' % remote_ip)

    return message

def worker(job_json, sender):
    """
    Parses the job dict into a MarketOrderList or MarketHistory instance.
    This gets dumped to JSON and sent on to the relays for sending to the
    subscribers.

    :param str job_json: The job dict from the broker/gateway.
    :param zmq.socket: The socket to send orders to the relays with.
    """
    order_list = parse_message(job_json)

    # Eventually, we'll do some sanity checking here.

    if order_list:
        json_str = unified.encode_to_json(order_list)
        #loaded = simplejson.loads(json_str)
        #print simplejson.dumps(loaded, indent=4)
        sender.send(zlib.compress(json_str))
