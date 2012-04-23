"""
Parser for the EVE Marketeer and EVE Market Data uploader format.
"""
import csv
import logging
from StringIO import StringIO
from emdr.core.market_data import MarketOrderList, MarketOrder
from emdr.core.serialization.common_utils import parse_datetime
from emdr.core.serialization.exceptions import InvalidMarketOrderDataError

logger = logging.getLogger(__name__)

def parse_from_payload(payload):
    """
    Given a job dict payload, parse the contents and return an
    :py:class:`src.core.market_data.MarketOrderList` instance, which contains
    :py:class:`src.core.market_data.MarketOrder` instances, each of which
    represents a market order.

    :param dict payload: A job dict.
    :rtype: MarketOrderList
    :returns: A MarketOrderList instance that contains MarketOrder instances.
    """
    log = payload['log']
    type_id = payload['type_id']
    region_id = payload['region_id']
    generated_at = payload['generated_at']
    order_generator = {
        'name': payload['developer_key'],
        'version': payload['version']
    }
    upload_keys = [{
        'name': 'EMDR',
        'key': payload['upload_key']
    }]

    # Orders are lumped into this list sub-class, which can be serialized
    # to JSON.
    order_list = MarketOrderList(
        order_generator=order_generator,
        upload_keys=upload_keys,
    )

    # Stuff the string here so the csv reader module can pull from it.
    # TODO: Look at getting the csv reader to read the string directly.
    log_buf = StringIO(log)

    # Parse the market log buffer as a CSV.
    for row in csv.reader(log_buf, delimiter=','):
        # This is pretty verbose, but we'll do it for the sake of there being
        # no question which column is barfing out (if we run into that).
        order_id = row[0]
        order_type = row[1]
        solar_system_id = row[2]
        station_id = row[3]
        price = row[4]
        volume_entered = row[5]
        volume_remaining = row[6]
        minimum_volume = row[7]
        order_issue_date = row[8]
        order_duration = row[9]
        order_range = row[10]

        # Now we cast each bit of data as a poor man's validator.
        order_id = int(order_id)

        if order_type == "s":
            is_bid = False
        elif order_type == "b":
            is_bid = True
        else:
            raise InvalidMarketOrderDataError(
                "Invalid order type (must be 's' or 'b'): %s" % order_type)

        # Sometimes these come in as floats, but they need to be ints.
        volume_remaining = int(float(volume_remaining))

        order_issue_date = parse_datetime(order_issue_date)
        data_generated_at = parse_datetime(generated_at)

        # Finally, instantiate and pop out a MarketOrder instance.
        order_list.add_order(MarketOrder(
            order_id, is_bid, region_id, solar_system_id, station_id,
            type_id, price, volume_entered, volume_remaining, minimum_volume,
            order_issue_date, order_duration, order_range,
            data_generated_at
        ))

    return order_list