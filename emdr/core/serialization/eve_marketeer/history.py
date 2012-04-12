"""
Parser for the EVE Marketeer and EVE Market Data uploader format.
"""
import csv
import logging
import datetime
from StringIO import StringIO
from emdr.core.market_data import MarketHistory, MarketHistoryEntry
from emdr.core.serialization.exceptions import InvalidMarketOrderDataError

logger = logging.getLogger(__name__)

def parse_from_payload(payload):
    """
    Given a job dict payload, parse the contents and return an
    :py:class:`src.core.market_data.MarketHistory` instance, which contains
    :py:class:`src.core.market_data.MarketHistoryEntry` instances, each of which
    represents a set of market history stats.

    :param dict payload: A job dict.
    :rtype: MarketHistory
    :returns: A MarketHistory instance that contains MarketHistoryEntry instances.
    """
    log = payload['log']
    upload_type = payload['upload_type']
    type_id = payload['type_id']
    region_id = payload['region_id']
    order_generator = {
        'name': payload['developer_key'],
        'version': payload['version']
    }

    # Orders are lumped into this list sub-class, which can be serialized
    # to JSON.
    history = MarketHistory(
        order_generator=order_generator
    )

    # Stuff the string here so the csv reader module can pull from it.
    # TODO: Look at getting the csv reader to read the string directly.
    log_buf = StringIO(log)

    if upload_type != 'history':
        # This isn't a history upload, we want no part in it.
        logger.error("Upload type other than 'history' found. Yuck.")
        return

    # Parse the market log buffer as a CSV.
    for row in csv.reader(log_buf, delimiter=','):
        historical_date,\
        low_price,\
        high_price,\
        average_price,\
        total_quantity,\
        num_orders = row

        # Now we cast each bit of data as a poor man's validator.
        historical_date = datetime.datetime.strptime(
            historical_date, "%Y-%m-%d")
        data_generated_at = datetime.datetime.now()

        # Finally, instantiate and pop out a MarketOrder instance, which will
        # be re-serialized in our standard format and sent to SQS for the
        # workers to pull and save.
        history.add_entry(MarketHistoryEntry(
            type_id, region_id, historical_date, num_orders, low_price,
            high_price, average_price, total_quantity,
            data_generated_at
        ))

    return history