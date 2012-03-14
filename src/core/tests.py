import unittest
import datetime
from src.core import market_data

class MarketOrderTests(unittest.TestCase):
    """
    Various tests for the market_data.MarketOrder class, which is our internal
    Python representation of a market order.
    """

    def setUp(self):
        self.order1 = market_data.MarketOrder(
            order_id=2413387906,
            order_type=market_data.ORDER_TYPE_BUY,
            region_id=10000068,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000068,
            price=52875.0,
            volume_entered=10,
            volume_remaining=4,
            minimum_volume=1,
            order_issue_date=datetime.datetime.now(),
            order_duration=90,
            order_range=5,
        )

    def test_json(self):
        """
        JSON encoding/de-coding tests.
        """
        # Encode the sample order.
        encoded_order1 = self.order1.to_json()
        # Should return a string JSON representation.
        self.assertIsInstance(encoded_order1, basestring)
        # De-code the JSON to instantiate a MarketOrder instance that should
        # be identical to self.order1.
        decoded_order1 = market_data.MarketOrder.from_json(encoded_order1)
        # Re-encode the decoded order1. Match the two encoded strings. They
        # should still be the same.
        self.assertEqual(encoded_order1, decoded_order1.to_json())