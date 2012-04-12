"""
Parser for the Unified uploader format market history.
"""
import logging
import datetime
import simplejson
from emdr.core.market_data import MarketHistory, MarketHistoryEntry
from emdr.core.serialization.unified.unified_utils import _columns_to_kwargs
from emdr.core.serialization.unified.unified_utils import parse_iso8601_str

logger = logging.getLogger(__name__)

# This is the standard list of columns to return data in for encoding.
STANDARD_ENCODED_COLUMNS = [
    'date', 'orders', 'quantity', 'low', 'high', 'average',
]

# This is a dict that acts like a mapping table, with the key being the
# Unified uploader format field name, and the value being the corresponding
# kwarg to the MarketOrder class. This lets us instantiate the class directly
# from the data.
SPEC_TO_KWARG_CONVERSION = {
    'date': 'historical_date',
    'orders': 'num_orders',
    'low': 'low_price',
    'high': 'high_price',
    'average': 'average_price',
    'quantity': 'total_quantity',
}

def parse_from_dict(json_dict):
    """
    Given a Unified Uploader message, parse the contents and return a
    MarketHistory instance.

    :param dict json_dict: A Unified Uploader message as a dict.
    :rtype: MarketOrderList
    :returns: An instance of MarketOrderList, containing the orders
        within.
    """
    history_columns = json_dict['columns']

    history = MarketHistory(
        upload_keys=json_dict['uploadKeys'],
        order_generator=json_dict['generator'],
    )

    for rowset in json_dict['rowsets']:
        generated_at = parse_iso8601_str(rowset['generatedAt'])
        region_id = rowset['regionID']
        type_id = rowset['typeID']

        for row in rowset['rows']:
            history_kwargs = _columns_to_kwargs(
                SPEC_TO_KWARG_CONVERSION, history_columns, row)
            historical_date = parse_iso8601_str(history_kwargs['historical_date'])

            history_kwargs.update({
                'type_id': type_id,
                'region_id': region_id,
                'historical_date': historical_date,
                'generated_at': generated_at,
            })

            history.add_entry(MarketHistoryEntry(**history_kwargs))

    return history

def encode_to_json(history_list):
    """
    Encodes this MarketHistory instance to a JSON string.

    :param MarketHistory history_list: The history instance to serialize.
    :rtype: str
    """
    rowsets = []
    for key, history_entries in history_list._history.items():
        rows = []
        for entry in history_entries:
            historical_date = entry.historical_date.replace(microsecond=0).isoformat()

            # The order in which these values are added is crucial. It must
            # match STANDARD_ENCODED_COLUMNS.
            rows.append([
                historical_date,
                entry.num_orders,
                entry.total_quantity,
                entry.low_price,
                entry.high_price,
                entry.average_price,
            ])

        #noinspection PyUnresolvedReferences
        rowsets.append(dict(
            generatedAt = datetime.datetime.now().replace(microsecond=0).isoformat(),
            regionID = history_entries[0].region_id,
            typeID = history_entries[0].type_id,
            rows = rows,
        ))

    json_dict = {
        'resultType': history_list.result_type,
        'version': history_list.version,
        'uploadKeys': history_list.upload_keys,
        'generator': history_list.history_generator,
        'currentTime': datetime.datetime.now().replace(microsecond=0).isoformat(),
        # This must match the order of the values in the row assembling portion
        # above this.
        'columns': STANDARD_ENCODED_COLUMNS,
        'rowsets': rowsets,
    }

    return simplejson.dumps(json_dict, indent=4 * ' ')