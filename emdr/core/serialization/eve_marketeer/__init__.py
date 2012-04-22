import logging
from emdr.core.serialization.eve_marketeer import history, orders
from emdr.daemons.gateway.exceptions import MalformedUploadError

logger = logging.getLogger(__name__)

def parse_from_payload(payload):
    """
    Given an EVE Marketeer message, parse the contents and return a
    MarketOrderList or MarketHistoryList instance. If a parser error is
    encountered, return None.

    :param dict payload: An EVE Marketeer payload dict from the gateway.
    :rtype: MarketOrderList or MarketHistoryList, or None.
    """
    # Some very basic sanity checking.
    for key, value in payload.items():
        if not value:
            raise MalformedUploadError(
                'EMK message missing key: %s' % key)

    upload_type = payload['upload_type']
    if upload_type == 'orders':
        return orders.parse_from_payload(payload)
    elif upload_type == 'history':
        return history.parse_from_payload(payload)
    else:
        raise MalformedUploadError(
            'EMK message has unknown upload_type: %s' % upload_type)