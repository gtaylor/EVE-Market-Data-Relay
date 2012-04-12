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
                {'name': 'eve-market-data-relay', 'key': 'default'},
            ]
        else:
            self.upload_keys = upload_keys

        if not order_generator:
            self.order_generator = {'name': 'Unknown', 'version': 'Unknown'}
        else:
            self.order_generator = order_generator

    def add_order(self, order):
        key = '%s_%s' % (order.is_bid, order.region_id)
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
                 station_id, type_id,
                 price, volume_entered, volume_remaining, minimum_volume,
                 order_issue_date, order_duration, order_range, generated_at):
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
