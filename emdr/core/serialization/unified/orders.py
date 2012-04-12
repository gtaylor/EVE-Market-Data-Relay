"""
Parser for the Unified uploader format orders.
"""
import logging
import datetime
import simplejson
from emdr.core.serialization.unified.unified_utils import parse_iso8601_str, _columns_to_kwargs
from emdr.core.market_data import MarketOrder
from emdr.core.market_data import MarketOrderList

logger = logging.getLogger(__name__)

# This is the standard list of columns to return data in for encoding.
STANDARD_ENCODED_COLUMNS = [
    'price', 'volRemaining', 'range', 'orderID', 'volEntered',
    'minVolume', 'bid', 'issueDate', 'duration', 'stationID',
    'solarSystemID',
]

# This is a dict that acts like a mapping table, with the key being the
# Unified uploader format field name, and the value being the corresponding
# kwarg to the MarketOrder class. This lets us instantiate the class directly
# from the data.
SPEC_TO_KWARG_CONVERSION = {
    'price': 'price',
    'volRemaining': 'volume_remaining',
    'range': 'order_range',
    'orderID': 'order_id',
    'volEntered': 'volume_entered',
    'minVolume': 'minimum_volume',
    'bid': 'is_bid',
    'issueDate': 'order_issue_date',
    'duration': 'order_duration',
    'stationID': 'station_id',
    'solarSystemID': 'solar_system_id',
}

def parse_from_dict(json_dict):
    """
    Given a Unified Uploader message, parse the contents and return a
    MarketOrderList.

    :param str json_str: A Unified Uploader message as a JSON string.
    :rtype: MarketOrderList
    :returns: An instance of MarketOrderList, containing the orders
        within.
    """
    order_columns = json_dict['columns']

    order_list = MarketOrderList(
        upload_keys=json_dict['uploadKeys'],
        order_generator=json_dict['generator'],
    )

    for rowset in json_dict['rowsets']:
        generated_at = parse_iso8601_str(rowset['generatedAt'])
        region_id = rowset['regionID']
        type_id = rowset['typeID']

        for row in rowset['rows']:
            order_kwargs = _columns_to_kwargs(
                SPEC_TO_KWARG_CONVERSION, order_columns, row)
            order_kwargs.update({
                'region_id': region_id,
                'type_id': type_id,
                'generated_at': generated_at,
            })

            order_kwargs['order_issue_date'] = parse_iso8601_str(order_kwargs['order_issue_date'])

            order_list.add_order(MarketOrder(**order_kwargs))

    return order_list

def encode_to_json(order_list):
    """
    Encodes this list of MarketOrder instances to a JSON string.

    :param MarketOrderList order_list: The order list to serialize.
    :rtype: str
    """
    rowsets = []
    for key, orders in order_list._orders.items():
        rows = []
        for order in orders:
            issue_date = order.order_issue_date.replace(microsecond=0).isoformat()

            # The order in which these values are added is crucial. It must
            # match STANDARD_ENCODED_COLUMNS.
            rows.append([
                order.price,
                order.volume_remaining,
                order.order_range,
                order.order_id,
                order.volume_entered,
                order.minimum_volume,
                order.is_bid,
                issue_date,
                order.order_duration,
                order.station_id,
                order.solar_system_id,
            ])

        #noinspection PyUnresolvedReferences
        rowsets.append(dict(
            generatedAt = datetime.datetime.now().replace(microsecond=0).isoformat(),
            regionID = orders[0].region_id,
            typeID = orders[0].type_id,
            rows = rows,
        ))

    json_dict = {
        'resultType': order_list.result_type,
        'version': order_list.version,
        'uploadKeys': order_list.upload_keys,
        'generator': order_list.order_generator,
        'currentTime': datetime.datetime.now().replace(microsecond=0).isoformat(),
        # This must match the order of the values in the row assembling portion
        # above this.
        'columns': STANDARD_ENCODED_COLUMNS,
        'rowsets': rowsets,
    }

    return simplejson.dumps(json_dict, indent=4 * ' ')