"""
Data structures for representing market data.
"""
from string import Template

# Some order type defines. Use these constants instead of "buy" and "sell"
# where possible.
ORDER_TYPE_BUY = "buy"
ORDER_TYPE_SELL = "sell"
ORDER_TYPES = [ORDER_TYPE_BUY, ORDER_TYPE_SELL]

class InvalidMarketOrderDataError(Exception):
    """
    Raise this when invalid market order data is passed into MarketOrder's
    constructor.
    """
    pass


class MarketOrder(object):
    """
    Represents a market buy or sell order.
    """

    def __init__(self, order_id, order_type, region_id, solar_system_id,
                 station_id, type_id,
                 price, volume_entered, volume_remaining, minimum_volume,
                 order_issue_date, order_duration, order_range):
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
        """
        self.order_id = order_id

        if order_type not in ORDER_TYPES:
            raise InvalidMarketOrderDataError("Invalid order type.")

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

    def __str__(self):
        """
        Basic string representation of the order.
        """
        template = Template(
            "Market Order: \n"
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
            " order_range: $order_range\n"
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
