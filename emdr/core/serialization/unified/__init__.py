import simplejson
from simplejson.decoder import JSONDecodeError
from emdr.core.market_data import MarketHistoryList
from emdr.core.market_data import MarketOrderList
from emdr.core.serialization.unified import history, orders
from emdr.daemons.gateway.exceptions import MalformedUploadError

def parse_from_json(json_str):
    """
    Given a Unified Uploader message, parse the contents and return a
    MarketOrderList or MarketHistoryList instance.

    :param str json_str: A Unified Uploader message as a JSON string.
    :rtype: MarketOrderList or MarketHistoryList
    :raises: MalformedUploadError when invalid JSON is passed in.
    """
    try:
        message_dict = simplejson.loads(json_str)
    except JSONDecodeError as exc:
        raise MalformedUploadError(exc.message)

    upload_type = message_dict['resultType']
    if upload_type == 'orders':
        return orders.parse_from_dict(message_dict)
    elif upload_type == 'history':
        return history.parse_from_dict(message_dict)
    else:
        raise MalformedUploadError(
            'Unified message has unknown upload_type: %s' % upload_type)

def encode_to_json(order_or_history):
    """
    Given an order or history entry, encode it to JSON and return.

    :type order_or_history: MarketOrderList or MarketHistoryList
    :param order_or_history: A MarketOrderList or MarketHistoryList instance to
        encode to JSON.
    :rtype: str
    :return: The encoded JSON string.
    """
    if isinstance(order_or_history, MarketOrderList):
        return orders.encode_to_json(order_or_history)
    elif isinstance(order_or_history, MarketHistoryList):
        return history.encode_to_json(order_or_history)
    else:
        raise Exception("Must be one of MarketOrderList or MarketHistoryList.")