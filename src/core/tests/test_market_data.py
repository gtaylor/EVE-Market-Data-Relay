import unittest
import datetime
from src.core import market_data
from src.core.market_data import MarketOrder, SerializableOrderList

class MarketOrderTests(unittest.TestCase):
    """
    Various tests for the market_data classes, which are our internal
    Python representations of a market orders.
    """
    def setUp(self):
        self.order1 = MarketOrder(
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
            generated_at=datetime.datetime.now()
        )
        self.order_list = SerializableOrderList()
        self.order_list.add_order(self.order1)

    def test_json(self):
        """
        JSON encoding/de-coding tests.
        """
        # Encode the sample order list.
        encoded_orderlist = self.order_list.to_json()
        print(encoded_orderlist)
        return
        # Should return a string JSON representation.
        self.assertIsInstance(encoded_orderlist, basestring)
        # De-code the JSON to instantiate a list of MarketOrder instances that
        # should be identical to self.orderlist.
        decoded_list = SerializableOrderList.from_json(encoded_orderlist)
        # Re-encode the decoded orderlist. Match the two encoded strings. They
        # should still be the same.
        self.assertEqual(encoded_orderlist, decoded_list.to_json())