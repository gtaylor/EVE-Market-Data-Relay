"""
The worker function in this module performs the order processing.
"""
import logging
import simplejson
from src.core.market_data import SerializableOrderList
from src.daemons.gateway import parsers

logger = logging.getLogger(__name__)

def parser_order(job_json):
    """
    Routes the order to the correct parser, returns the parsed order in
    Unified Uploader format.

    :param str job_json: A raw JSON job dict string to parse.
    :rtype: SerializableOrderList
    :returns: A serializable list of MarketOrder objects.
    """
    job_dict = simplejson.loads(job_json)
    # Orders are lumped into this list sub-class, which has JSON-serialization
    # methods on it.
    order_list = SerializableOrderList()

    # The format attrib on the job dict determines which parser to use.
    order_format = job_dict.get('format', 'unknown')

    try:
        # A payload must exist, regardless of the format. The payload contains
        # the data passed to the gateway.
        payload = job_dict['payload']
    except KeyError:
        logger.error('Job dict has no payload key. Discarding.')
        return

    if order_format == 'eve_marketeer':
        order_generator = parsers.eve_marketeer.parse_from_payload(payload)
    else:
        logger.error('Unknown order format encountered. Discarding.')
        return

    # This generator spits out the MarketOrder instances that user sent. Since
    # one item can have many orders, we add each order entry to our
    # SerializableOrderList instance.
    for order in order_generator:
        order_list.append(order)

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

    order_list = parser_order(job_json)
    if order_list:
        sender.send(order_list.to_json())
