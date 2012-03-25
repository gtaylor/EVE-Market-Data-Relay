"""
Parser for the Unified uploader format.
"""
import logging
import datetime
import simplejson
from src.core.market_data import MarketOrder, ORDER_TYPE_BUY, ORDER_TYPE_SELL
from src.core.market_data import SerializableOrderList

logger = logging.getLogger(__name__)

SPEC_TO_KWARG_CONVERSION = {
    'price': 'price',
    'volRemaining': 'volume_remaining',
    'range': 'order_range',
    'orderID': 'order_id',
    'volEntered': 'volume_entered',
    'minVolume': 'minimum_volume',
    'bid': 'order_type',
    'issueDate': 'order_issue_date',
    'duration': 'order_duration',
    'stationID': 'station_id',
    'solarSystemID': 'solar_system_id',
    }
# Do the reverse.
KWARG_TO_SPEC_CONVERSION = {}
for key, item in SPEC_TO_KWARG_CONVERSION.items():
    KWARG_TO_SPEC_CONVERSION[item] = key

def _columns_to_kwargs(columns, row):
    kwdict = {}

    counter = 0
    for column in columns:
        kwarg_name = SPEC_TO_KWARG_CONVERSION[column]
        kwdict[kwarg_name] = row[counter]
        counter += 1

    return kwdict

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
    json_dict = simplejson.loads(payload['body'])

    order_list = SerializableOrderList(
        upload_keys=json_dict['uploadKeys'],
        order_generator=json_dict['generator'],
        columns=json_dict['columns'],
    )

    for rowset in json_dict['rowsets']:
        generated_at = rowset['generatedAt']
        region_id = rowset['regionID']
        type_id = rowset['typeID']

        for row in rowset['rows']:
            order_kwargs = _columns_to_kwargs(order_list.columns, row)
            order_kwargs.update({
                'region_id': region_id,
                'type_id': type_id,
                'generated_at': generated_at,
            })
            order_list.add_order(MarketOrder(**order_kwargs))

    return order_list

def order_list_to_json(order_list):
    """
    Encodes this list of MarketOrder instances to a JSON string.

    :rtype: str
    """
    rowsets = []
    for key, orders in order_list._orders.items():
        rows = []
        for order in orders:
            issue_date = datetime.datetime.strftime(
                order.order_issue_date, "%Y-%m-%d %H:%M:%S")

            rows.append([
                order.price,
                order.volume_remaining,
                order.order_range,
                order.order_id,
                order.volume_entered,
                order.minimum_volume,
                order.order_type,
                issue_date,
                order.order_duration,
                order.station_id,
                order.solar_system_id,
                ])

        #noinspection PyUnresolvedReferences
        rowsets.append(dict(
            generatedAt = datetime.datetime.strftime(
                orders[0].order_issue_date, "%Y-%m-%d %H:%M:%S"),
            regionID = orders[0].region_id,
            typeID = orders[0].type_id,
            rows = rows,
        ))

    json_dict = {
        'resultType': order_list.result_type,
        'version': order_list.version,
        'uploadKeys': order_list.upload_keys,
        'generator': order_list.order_generator,
        'currentTime': 'TESTING',
        'columns': order_list.columns,
        'rowsets': rowsets,
    }

    return simplejson.dumps(json_dict, indent=4 * ' ')