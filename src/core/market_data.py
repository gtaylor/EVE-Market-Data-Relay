"""
Data structures for representing market data.
"""
import datetime
import simplejson
from string import Template

# Some order type defines. Use these constants instead of "buy" and "sell"
# where possible.
ORDER_TYPE_BUY = "buy"
ORDER_TYPE_SELL = "sell"
ORDER_TYPES = [ORDER_TYPE_BUY, ORDER_TYPE_SELL]

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

class SerializableOrderList(object):
    """
    A list of MarketOrder objects, with some convenience methods for
    serialization.
    """
    result_type = "orders"
    version = "0.1alpha"

    def __init__(self, upload_keys=None, order_generator=None, columns=None,
                 *args, **kwargs):
        self._orders = {}

        if not upload_keys:
            self.upload_keys = [
                {'name': 'eve-market-data-relay', 'key': 'default'},
            ]
        else:
            self.upload_keys = upload_keys

        if not order_generator:
            self.order_generator = {'name': 'Unknown', 'version': 'Unknown'}
        else:
            self.order_generator = order_generator

        if not columns:
            self.columns = [
                'price', 'volRemaining', 'range', 'orderID', 'volEntered',
                'minVolume', 'bid', 'issueDate', 'duration', 'stationID',
                'solarSystemID',
            ]
        else:
            self.columns = columns

    def add_order(self, order):
        key = '%s_%s' % (order.order_type, order.region_id)
        if not self._orders.has_key(key):
            self._orders[key] = []

        self._orders[key].append(order)

    def to_json(self):
        """
        Encodes this list of MarketOrder instances to a JSON string.

        :rtype: str
        """
        rowsets = []
        for key, orders in self._orders.items():
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
            'resultType': self.result_type,
            'version': self.version,
            'uploadKeys': self.upload_keys,
            'generator': self.order_generator,
            'currentTime': 'TESTING',
            'columns': self.columns,
            'rowsets': rowsets,
        }

        return simplejson.dumps(json_dict, indent=4 * ' ')

    def _columns_to_kwargs(self, columns, row):
        kwdict = {}

        counter = 0
        for column in columns:
            kwarg_name = SPEC_TO_KWARG_CONVERSION[column]
            kwdict[kwarg_name] = row[counter]
            counter += 1

        return kwdict

    @staticmethod
    def from_json(json_str):
        """
        Convenience method used to de-code a JSON string to a
        SerializableOrderList instance that contains MarketOrder instances.

        :rtype: SerializableOrderList
        """
        json_dict = simplejson.loads(json_str)

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
                order_kwargs = order_list._columns_to_kwargs(
                    order_list.columns, row
                )
                order_kwargs.update({
                    'region_id': region_id,
                    'type_id': type_id,
                    'generated_at': generated_at,
                })
                order_list.add_order(MarketOrder(**order_kwargs))

        return order_list

class MarketOrder(object):
    """
    Represents a market buy or sell order.
    """
    def __init__(self, order_id, order_type, region_id, solar_system_id,
                 station_id, type_id,
                 price, volume_entered, volume_remaining, minimum_volume,
                 order_issue_date, order_duration, order_range, generated_at):
        """
        :param int order_id: The unique order ID for this order.
        :param str order_type: One of 'buy' or 'sell'.
        :param int region_id: The region the order is in.
        :param int solar_system_id: The solar system the order is in.
        :param int station_id: The station the order is in.
        :param int type_id: The item type of the order.
        :param float price: The buy/sell price per item.
        :param int volume_entered: The original amount of the buy/sell order.
        :param int volume_remaining: The quantity remaining in the order.
        :param int minimum_volume: The minimum volume that may remain
            before the order is removed.
        :param datetime order_issue_date: The time at which the order was
            first posted.
        :param int order_duration: The duration (in days) of the order.
        :param int order_range: No idea what this is.
        :param datetime.datetime generated_at: Time of generation.
        """
        self.order_id = order_id
        self.order_type = order_type
        self.region_id = region_id
        self.solar_system_id = solar_system_id
        self.station_id = station_id
        self.type_id = type_id
        self.price = price
        self.volume_entered = volume_entered
        self.volume_remaining = volume_remaining
        self.minimum_volume = minimum_volume
        self.order_issue_date = order_issue_date
        self.order_duration = order_duration
        self.order_range = order_range
        self.generated_at = generated_at

    def __repr__(self):
        """
        Basic string representation of the order.
        """
        template = Template(
            "<Market Order: \n"
            " order_id: $order_id\n"
            " order_type: $order_type\n"
            " region_id: $region_id\n"
            " solar_system_id: $solar_system_id\n"
            " station_id: $station_id\n"
            " type_id: $type_id\n"
            " price: $price\n"
            " volume_entered: $volume_entered\n"
            " volume_remaining: $volume_remaining\n"
            " minimum_volume: $minimum_volume\n"
            " order_issue_date: $order_issue_date\n"
            " order_duration: $order_duration\n"
            " order_range: $order_range>\n"
        )
        return template.substitute(
            order_id = self.order_id,
            order_type = self.order_type,
            region_id = self.region_id,
            solar_system_id = self.solar_system_id,
            station_id = self.station_id,
            type_id = self.type_id,
            price = self.price,
            volume_entered = self.volume_entered,
            volume_remaining = self.volume_remaining,
            minimum_volume = self.minimum_volume,
            order_issue_date = self.order_issue_date,
            order_duration = self.order_duration,
            order_range = self.order_range,
        )
