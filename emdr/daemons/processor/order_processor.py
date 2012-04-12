"""
The worker function in this module performs the order processing.
"""
import logging
import zlib
import simplejson
from emdr.core import serialization

logger = logging.getLogger(__name__)

def parse_order(job_json):
    """
    Routes the order to the correct parser, returns the parsed order in
    Unified Uploader format.

    :param str job_json: A raw JSON job dict string to parse.
    :rtype: SerializableOrderList
    :returns: A serializable list of MarketOrder objects.
    """
    job_dict = simplejson.loads(zlib.decompress(job_json))

    # The format attrib on the job dict determines which parser to use.
    order_format = job_dict.get('format', 'unknown')

    try:
        # A payload must exist, regardless of the format. The payload contains
        # the data passed to the gateway.
        payload = job_dict['payload']
    except KeyError:
        logger.error('Job dict has no payload key. Discarding.')
        return

    if order_format == 'unified':
        order_list = serialization.unified.parse_from_json(payload['body'])
    elif order_format == 'eve_marketeer':
        order_list = serialization.eve_marketeer.parse_from_payload(payload)
    else:
        logger.error('Unknown order format encountered. Discarding.')
        return

    return order_list

def worker(job_json, sender):
    """
    Parses the job dict into a SerializableOrderList of MarketOrder instances.
    This gets dumped to JSON and sent on to the relays for sending to the
    subscribers.

    :param str job_json: The job dict from the broker/gateway.
    :param zmq.socket: The socket to send orders to the relays with.
    """
    logger.info('Processing one job.')

    order_list = parse_order(job_json)
    print order_list
    if order_list:
        json_str = serialization.unified.encode_to_json(order_list)
        sender.send(zlib.compress(json_str))
