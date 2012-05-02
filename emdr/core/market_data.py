"""
Data structures for representing market data.
"""
import datetime
from string import Template

class MarketOrderList(object):
    """
    A list of MarketOrder objects, with some added features for assisting
    with serializing to the Unified Uploader Interchange format.
    """
    result_type = "orders"
    # Unified market data format revision.
    version = "0.1alpha"

    def __init__(self, upload_keys=None, order_generator=None,
                 *args, **kwargs):
        self._orders = {}

        if not upload_keys:
            self.upload_keys = [
                {'name': 'EMDR', 'key': 'default'},
            ]
        else:
            self.upload_keys = upload_keys

            if not isinstance(self.upload_keys, list):
                raise TypeError('upload_keys must be a list.')

        if not order_generator:
            self.order_generator = {'name': 'Unknown', 'version': 'Unknown'}
        else:
            self.order_generator = order_generator

            if not isinstance(order_generator, dict):
                raise TypeError('order_generator must be a dict.')

    def add_order(self, order):
        """
        Adds a MarketOrder instance to the list of market orders contained
        within this order list. Does some behind-the-scenes magic to get it
        all ready for serialization.

        :param MarketOrder order: The order to add to this order list.
        """
        # This key is used to group the orders based on region.
        key = '%s_%s' % (order.region_id, order.type_id)
        if not self._orders.has_key(key):
            self._orders[key] = []

        self._orders[key].append(order)

    def __repr__(self):
        """
        Basic string representation of the order.
        """
        template = Template(
            "<MarketOrderList: \n"
            " upload_keys: $upload_keys\n"
            " order_generator: $order_generator\n"
        )
        list_repr = template.substitute(
            upload_keys = self.upload_keys,
            order_generator = self.order_generator,
        )
        for order_list in self._orders.values():
            for order in order_list:
                list_repr += repr(order)

        return list_repr

class MarketOrder(object):
    """
    Represents a market buy or sell order.
    """
    def __init__(self, order_id, is_bid, region_id, solar_system_id,
                 station_id, type_id, price, volume_entered, volume_remaining,
                 minimum_volume, order_issue_date, order_duration, order_range,
                 generated_at):
        """
        :param int order_id: The unique order ID for this order.
        :param bool is_bid: If ``True``, this is a bid (buy order). If ``False``,
            it's a sell order.
        :param int region_id: The region the order is in.
        :param int solar_system_id: The solar system the order is in.
        :param int station_id: The station the order is in.
        :param int type_id: The item type of the order.
        :param float price: The buy/sell price per item.
        :param int volume_entered: The original amount of the buy/sell order.
        :param int volume_remaining: The quantity remaining in the order.
        :param int minimum_volume: The minimum volume that may remain
            before the order is removed.
        :param datetime.datetime order_issue_date: The time at which the order
            was first posted.
        :param int order_duration: The duration (in days) of the order.
        :param int order_range: No idea what this is.
        :param datetime.datetime generated_at: Time of generation.
        """
        self.order_id = int(order_id)
        if not isinstance(is_bid, bool):
            raise TypeError('is_bid should be a bool.')
        self.is_bid = is_bid
        if region_id:
            self.region_id = int(region_id)
        else:
            # Client lacked the data for result rows.
            self.region_id = None
        if solar_system_id:
            self.solar_system_id = int(solar_system_id)
        else:
            # Client lacked the data for result rows.
            self.solar_system_id = None
        self.station_id = int(station_id)
        self.type_id = int(type_id)
        self.price = float(price)
        self.volume_entered = int(volume_entered)
        self.volume_remaining = int(volume_remaining)
        self.minimum_volume = int(minimum_volume)
        if not isinstance(order_issue_date, datetime.datetime):
            raise TypeError('order_issue_date should be a datetime.')
        self.order_issue_date = order_issue_date
        self.order_duration = int(order_duration)
        self.order_range = int(order_range)
        if not isinstance(generated_at, datetime.datetime):
            raise TypeError('generated_at should be a datetime.')
        self.generated_at = generated_at

    def __repr__(self):
        """
        Basic string representation of the order.
        """
        template = Template(
            "<Market Order: \n"
            " order_id: $order_id\n"
            " is_bid: $is_bid\n"
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
            is_bid = self.is_bid,
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

class MarketHistoryList(object):
    """
    A class for storing market order history for serialization.
    """
    result_type = "history"
    # Unified market data format revision.
    version = "0.1alpha"

    def __init__(self, upload_keys=None, history_generator=None,
                 *args, **kwargs):
        # Will hold an organized store of history items.
        self._history = {}

        if not upload_keys:
            self.upload_keys = [
                {'name': 'eve-market-data-relay', 'key': 'default'},
            ]
        else:
            self.upload_keys = upload_keys

            if not isinstance(self.upload_keys, list):
                raise TypeError('upload_keys must be a list.')

        if not history_generator:
            self.history_generator = {'name': 'Unknown', 'version': 'Unknown'}
        else:
            self.history_generator = history_generator

            if not isinstance(history_generator, dict):
                raise TypeError('history_generator must be a dict.')

    def __repr__(self):
        """
        Basic string representation of the history.
        """
        template = Template(
            "<MarketHistoryList: \n"
            " upload_keys: $upload_keys\n"
            " order_generator: $order_generator\n"
        )
        list_repr = template.substitute(
            upload_keys = self.upload_keys,
            order_generator = self.history_generator,
        )
        for history_entry_list in self._history.values():
            for entry in history_entry_list:
                list_repr += repr(entry)

        return list_repr

    def add_entry(self, entry):
        """
        Adds a MarketHistoryEntry instance to the list of market history entries
        contained within this instance. Does some behind-the-scenes magic to
        get it all ready for serialization.

        :param MarketHistoryEntry entry: The history entry to add to
            instance.
        """
        # This key is used to group the entries based on region and type.
        key = '%s_%s' % (entry.region_id, entry.type_id)
        if not self._history.has_key(key):
            self._history[key] = []

        self._history[key].append(entry)


class MarketHistoryEntry(object):
    """
    Represents a single point of market history data.
    """
    def __init__(self, type_id, region_id, historical_date, num_orders,
                 low_price, high_price, average_price, total_quantity,
                 generated_at):
        self.type_id = int(type_id)
        if region_id:
            self.region_id = int(region_id)
        else:
            # Client lacked the data for result rows.
            self.region_id = None
        if not isinstance(historical_date, datetime.datetime):
            raise TypeError('historical_date should be a datetime, not %s.' % type(historical_date))
        self.historical_date = historical_date
        self.num_orders = int(num_orders)
        self.low_price = float(low_price)
        self.high_price = float(high_price)
        self.average_price = float(average_price)
        self.total_quantity = int(total_quantity)
        if not isinstance(generated_at, datetime.datetime):
            raise TypeError('generated_at should be a datetime.')
        self.generated_at = generated_at

    def __repr__(self):
        """
        Basic string representation of the history entry.
        """
        template = Template(
            "<Market History Entry: \n"
            " type_id: $type_id\n"
            " region_id: $region_id\n"
            " historical_date: $historical_date\n"
            " num_orders: $num_orders\n"
            " low_price: $low_price\n"
            " high_price: $high_price\n"
            " average_price: $average_price\n"
            " total_quantity: $total_quantity\n"
            " generated_at: $generated_at\n"
        )
        return template.substitute(
            type_id = self.type_id,
            region_id = self.region_id,
            historical_date = self.historical_date,
            num_orders = self.num_orders,
            low_price = self.low_price,
            high_price = self.high_price,
            average_price = self.average_price,
            total_quantity = self.total_quantity,
            generated_at = self.generated_at,
        )