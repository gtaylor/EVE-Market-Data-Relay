"""
Parser for the EVE Marketeer and EVE Market Data uploader format.
"""
import csv
import logging
from StringIO import StringIO
from emdr.core.market_data import MarketHistoryList, MarketHistoryEntry
from emdr.core.serialization.common_utils import parse_datetime

logger = logging.getLogger(__name__)

def parse_from_payload(payload):
    """
    Given a job dict payload, parse the contents and return an
    :py:class:`src.core.market_data.MarketHistoryList` instance, which contains
    :py:class:`src.core.market_data.MarketHistoryEntry` instances, each of which
    represents a set of market history stats.

    :param dict payload: A job dict.
    :rtype: MarketHistoryList
    :returns: A MarketHistoryList instance that contains
        MarketHistoryEntry instances.
    """
    log = payload['log']
    type_id = payload['type_id']
    region_id = payload['region_id']
    generated_at = payload['generated_at']
    order_generator = {
        'name': payload['developer_key'],
        'version': payload['version']
    }
    upload_keys = {
        'name': 'EMDR',
        'key': payload['upload_key']
    }

    # Orders are lumped into this list sub-class, which can be serialized
    # to JSON.
    history = MarketHistoryList(
        history_generator=order_generator,
        upload_keys=upload_keys,
    )

    # Stuff the string here so the csv reader module can pull from it.
    # TODO: Look at getting the csv reader to read the string directly.
    log_buf = StringIO(log)

    # Parse the market log buffer as a CSV.
    for row in csv.reader(log_buf, delimiter=','):
        historical_date,\
        low_price,\
        high_price,\
        average_price,\
        total_quantity,\
        num_orders = row

        # The incoming data is just a date, so this ends up being hour/minute 0.
        historical_date = parse_datetime(historical_date)
        data_generated_at = parse_datetime(generated_at)

        # Finally, instantiate and pop out a MarketHistoryEntry instance.
        history.add_entry(MarketHistoryEntry(
            type_id, region_id, historical_date, num_orders, low_price,
            high_price, average_price, total_quantity,
            data_generated_at
        ))

    return history