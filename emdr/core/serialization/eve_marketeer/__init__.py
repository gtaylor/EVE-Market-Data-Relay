import logging
from emdr.core.serialization.eve_marketeer import history, orders

logger = logging.getLogger(__name__)

def parse_from_payload(payload):
    """
    Given an EVE Marketeer message, parse the contents and return a
    MarketOrderList or MarketHistory instance. If a parser error is encountered,
    return None.

    :param dict payload: An EVE Marketeer payload dict from the gateway.
    :rtype: MarketOrderList or MarketHistory, or None.
    """
    upload_type = payload['upload_type']
    if upload_type == 'orders':
        return orders.parse_from_payload(payload)
    elif upload_type == 'history':
        return history.parse_from_payload(payload)
    else:
        logger.error('Unknown upload_type: %s' % upload_type)
        return