"""
Tests for the full wsgi.py module, and all of its submodules.
"""
import unittest
import datetime
from emdr.core.market_data import MarketOrder, MarketOrderList

class GatewayWSGITests(unittest.TestCase):
    """
    Various tests for the gateway WSGI application.
    """
    def setUp(self):
        self.order1 = MarketOrder(
            order_id=2413387906,
            is_bid=True,
            region_id=10000068,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000068,
            price=52875.0,
            volume_entered=10,
            volume_remaining=4,
            minimum_volume=1,
            order_issue_date=datetime.datetime.utcnow(),
            order_duration=90,
            order_range=5,
            generated_at=datetime.datetime.utcnow(),
        )
        self.order_list = MarketOrderList()
        self.order_list.add_order(self.order1)
