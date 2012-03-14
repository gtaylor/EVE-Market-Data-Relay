"""
Parser for the EVE Marketeer and EVE Market Data uploader format.
"""
import csv
import logging
import datetime
from StringIO import StringIO
from src.core.market_data import MarketOrder, ORDER_TYPE_BUY, ORDER_TYPE_SELL

logger = logging.getLogger(__name__)

def parse_from_request(request):
    """
    Given a request, parse the contents and return a generator of
    :py:class:`src.core.market_data.MarketOrder` instances. Each instance
    represents a market order.
    """
    #print "FORMS", request.forms.items()

    # This is a CSV string that has line breaks as line separators.
    log = request.forms.log
    # Stuff the string here so the csv reader module can pull from it.
    # TODO: Look at getting the csv reader to read the string directly.
    log_buf = StringIO(log)

    upload_type = request.forms.upload_type
    if upload_type != 'orders':
        # This isn't an orders upload, we want no part in it.
        logger.error("Upload type other than 'order' found. Yuck.")
        return

    # The item type ID.
    type_id = request.forms.type_id
    region_id = request.forms.region_id
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
        order_type = ORDER_TYPE_BUY if order_type == "b" else ORDER_TYPE_SELL
        solar_system_id = int(solar_system_id)
        station_id = int(station_id)
        price = float(price)
        volume_entered = int(volume_entered)
        volume_remaining = int(float(volume_remaining))
        minimum_volume = int(minimum_volume)
        order_issue_date = datetime.datetime.strptime(
            order_issue_date, "%Y-%m-%d %H:%M:%S")
        order_duration = int(order_duration)
        order_range = int(order_range)

        # Finally, instantiate and pop out a MarketOrder instance, which will
        # be re-serialized in our standard format and sent to SQS for the
        # workers to pull and save.
        yield MarketOrder(
            order_id, order_type, region_id, solar_system_id, station_id,
            type_id, price, volume_entered, volume_remaining, minimum_volume,
            order_issue_date, order_duration, order_range,
        )