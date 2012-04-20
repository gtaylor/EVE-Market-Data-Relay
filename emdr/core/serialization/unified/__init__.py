import simplejson
from simplejson.decoder import JSONDecodeError
from emdr.core.market_data import MarketHistory
from emdr.core.market_data import MarketOrderList
from emdr.core.serialization.unified import history, orders

def parse_from_json(json_str):
    """
    Given a Unified Uploader message, parse the contents and return a
    MarketOrderList or MarketHistory instance.

    :param str json_str: A Unified Uploader message as a JSON string.
    :rtype: MarketOrderList or MarketHistory
    """
    try:
        job_dict = simplejson.loads(json_str)
    except JSONDecodeError:
        print "PARSE ERROR"
        print json_str

    if job_dict['resultType'] == 'orders':
        return orders.parse_from_dict(job_dict)
    else:
        return history.parse_from_dict(job_dict)

def encode_to_json(order_or_history):
    """
    Given an order or history entry, encode it to JSON and return.

    :type order_or_history: MarketOrderList or MarketHistory
    :param order_or_history: A MarketOrderList or MarketHistory instance to
        encode to JSON.
    :rtype: str
    :return: The encoded JSON string.
    """
    if isinstance(order_or_history, MarketOrderList):
        return orders.encode_to_json(order_or_history)
    elif isinstance(order_or_history, MarketHistory):
        return history.encode_to_json(order_or_history)
    else:
        raise Exception("Must be one of MarketOrderList or MarketHistory.")