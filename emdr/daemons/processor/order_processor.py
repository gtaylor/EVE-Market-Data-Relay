"""
The worker function in this module performs the order and history processing.
"""
import logging
import zlib
import simplejson
from simplejson.decoder import JSONDecodeError
from emdr.core.serialization import unified
from emdr.core.serialization import eve_marketeer
from emdr.core.serialization.exceptions import MessageParserError, InvalidMarketOrderDataError

logger = logging.getLogger(__name__)

def parse_message(message_json):
    """
    Routes the order or history message to the correct parser, returns the
    parsed order or history in Unified Uploader format. If an error is
    encountered, don't return anything.

    :param str message_json: A raw JSON message dict string to parse.
    :rtype: MarketOrderList or MarketHistory, or None
    :returns: A serializable MarketOrderList or MarketHistory instance.
    """
    message_dict = simplejson.loads(zlib.decompress(message_json))

    # The remote address who sent the message. This can be spoofed.
    remote_ip = message_dict['remote_address']
    # The format attrib on the message dict determines which parser to use.
    message_format = message_dict.get('format', 'unknown')

    try:
        # A payload must exist, regardless of the format. The payload contains
        # the data passed to the gateway.
        payload = message_dict['payload']
    except KeyError:
        logger.error('Message dict from %s has no payload key.' % remote_ip)
        return

    try:
        if message_format == 'unified':
            message = unified.parse_from_json(payload['body'])
        elif message_format == 'eve_marketeer':
            message = eve_marketeer.parse_from_payload(payload)
        else:
            # We don't support whatever format this is.
            logger.error('Unknown message format encountered in message from %s.' % remote_ip)
            return
    except (MessageParserError, JSONDecodeError):
        # Can't parse the message. It's mal-formed beyond any use.
        logger.error('Parsing error encountered in message (%s) from %s.' % (
            message_format, remote_ip
        ))
        return
    except InvalidMarketOrderDataError:
        # Message was parsed successfully, but one of the values was bogus.
        logger.error('Invalid or mal-formed message (%s) from %s.' % (
            message_format, remote_ip
        ))
        return

    if message:
        logger.info('%s (%s) from %s processed.' % (
            message.__class__.__name__,
            message_format,
            remote_ip
        ))
    else:
        # Error would have been logged elsewhere.
        return

    return message

def worker(message_json, sender):
    """
    Parses the message dict into a MarketOrderList or MarketHistory instance.
    This gets dumped to JSON and sent on to the relays for sending to the
    subscribers.

    :param str message_json: The message dict from the broker/gateway.
    :param zmq.socket: The socket to send orders to the relays with.
    """
    order_list = parse_message(message_json)

    if order_list:
        json_str = unified.encode_to_json(order_list)
        #loaded = simplejson.loads(json_str)
        #print simplejson.dumps(loaded, indent=4)
        sender.send(zlib.compress(json_str))
