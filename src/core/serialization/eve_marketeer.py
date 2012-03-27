"""
Parser for the EVE Marketeer and EVE Market Data uploader format.
"""
import csv
import logging
import datetime
from StringIO import StringIO
from src.core.market_data import SerializableOrderList, MarketOrder
from src.core.serialization.exceptions import InvalidMarketOrderDataError

logger = logging.getLogger(__name__)

def parse_from_payload(payload):
    """
    Given a job dict payload, parse the contents and return an
    SerializableOrderList instance, which contains
    :py:class:`src.core.market_data.MarketOrder` instances, each of which
    represents a market order.

    :param dict payload: A job dict.
    :rtype: SerializableOrderList
    :returns: A SerializableOrderList instance that contains MarketOrder instances.
    """
    log = payload['log']
    upload_type = payload['upload_type']
    type_id = payload['type_id']
    region_id = payload['region_id']
    order_generator = {'name': payload['developer_key'], 'version': payload['version']}

    # Orders are lumped into this list sub-class, which can be serialized
    # to JSON.
    order_list = SerializableOrderList(
        order_generator=order_generator
    )

    # Stuff the string here so the csv reader module can pull from it.
    # TODO: Look at getting the csv reader to read the string directly.
    log_buf = StringIO(log)

    if upload_type != 'orders':
        # This isn't an orders upload, we want no part in it.
        logger.error("Upload type other than 'orders' found. Yuck.")
        return

    # Parse the market log buffer as a CSV.
    for row in csv.reader(log_buf, delimiter=','):
        order_id,\
        order_type,\
        solar_system_id,\
        station_id,\
        price,\
        volume_entered,\
        volume_remaining,\
        minimum_volume,\
        order_issue_date,\
        order_duration,\
        order_range = row

        # Now we cast each bit of data as a poor man's validator.
        order_id = int(order_id)

        if order_type == "s":
            is_bid = False
        elif order_type == "b":
            is_bid = True
        else:
            raise InvalidMarketOrderDataError("Invalid order type.")

        order_issue_date = datetime.datetime.strptime(
            order_issue_date, "%Y-%m-%d %H:%M:%S")
        data_generated_at = datetime.datetime.now()

        # Finally, instantiate and pop out a MarketOrder instance, which will
        # be re-serialized in our standard format and sent to SQS for the
        # workers to pull and save.
        order_list.add_order(MarketOrder(
            order_id, is_bid, region_id, solar_system_id, station_id,
            type_id, price, volume_entered, volume_remaining, minimum_volume,
            order_issue_date, order_duration, order_range,
            data_generated_at
        ))

    return order_list