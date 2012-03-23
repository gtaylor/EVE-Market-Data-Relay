"""
Parser for the Unified uploader format.
"""
import logging
import datetime
import simplejson
from src.core.market_data import MarketOrder, ORDER_TYPE_BUY, ORDER_TYPE_SELL
from src.core.market_data import SerializableOrderList
from src.daemons.gateway.parsers.exceptions import InvalidMarketOrderDataError

logger = logging.getLogger(__name__)

def parse_from_payload(payload):
    """
    Given a job dict payload, parse the contents and return a generator of
    :py:class:`src.core.market_data.MarketOrder` instances. Each instance
    represents a market order.

    :param dict payload: A job dict.
    :rtype: generator
    :returns: A generator that pops out
        :py:class:`src.core.market_data.MarketOrder` instances.
    """
    order_list = SerializableOrderList()

    odata = simplejson.loads(payload['body'])

    for item in odata['rowsets']:
        # Finally, instantiate and pop out a MarketOrder instance, which will
        # be re-serialized in our standard format and sent to SQS for the
        # workers to pull and save.

        region_id = item['regionID']
        type_id = item['typeID']

        for order in item['rows']:
            price,\
            volume_remaining,\
            order_range, \
            order_id,\
            volume_entered,\
            minimum_volume, \
            bid,\
            order_issue_date,\
            order_duration,\
            station_id,\
            solar_system_id = order

            order_type = ORDER_TYPE_BUY if bid else ORDER_TYPE_SELL

            order_list.append(MarketOrder(
                order_id, order_type, region_id, solar_system_id, station_id,
                type_id, price, volume_entered, volume_remaining, minimum_volume,
                order_issue_date, order_duration, order_range,
            ))

    return order_list