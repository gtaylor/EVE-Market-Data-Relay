import unittest
import datetime
from emdr.core.market_data import MarketOrder, MarketOrderList, MarketHistoryList, MarketHistoryEntry
from emdr.core.serialization import unified

class BaseSerializationCase(unittest.TestCase):

    def setUp(self):
        self.order_list = MarketOrderList()
        self.order1 = MarketOrder(
            order_id=2413387906,
            is_bid=True,
            region_id=10000068,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000068,
            price=52875,
            volume_entered=10,
            volume_remaining=4,
            minimum_volume=1,
            order_issue_date=datetime.datetime.utcnow(),
            order_duration=90,
            order_range=5,
            generated_at=datetime.datetime.utcnow()
        )
        self.order_list.add_order(self.order1)
        self.order2 = MarketOrder(
            order_id=1234566,
            is_bid=False,
            region_id=10000032,
            solar_system_id=30005312,
            station_id=60011121,
            type_id=10000067,
            price=52,
            volume_entered=10,
            volume_remaining=500,
            minimum_volume=1,
            order_issue_date=datetime.datetime.utcnow(),
            order_duration=90,
            order_range=5,
            generated_at=datetime.datetime.utcnow()
        )
        self.order_list.add_order(self.order2)

        self.history = MarketHistoryList()
        self.history1 = MarketHistoryEntry(
            type_id=2413387906,
            region_id=10000068,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        )
        self.history.add_entry(self.history1)
        self.history2 = MarketHistoryEntry(
            type_id=1413387203,
            region_id=10000067,
            historical_date=datetime.datetime.utcnow(),
            num_orders=50,
            low_price=50.0,
            high_price=100.5,
            average_price=70.0,
            total_quantity=2000,
            generated_at=datetime.datetime.utcnow(),
        )
        self.history.add_entry(self.history2)

class UnifiedSerializationTests(BaseSerializationCase):
    """
    Tests for serializing and de-serializing orders in Unified format.
    """

    def test_order_serialization(self):
        # Encode the sample order list.
        encoded_orderlist = unified.encode_to_json(self.order_list)
        # Should return a string JSON representation.
        self.assertIsInstance(encoded_orderlist, basestring)
        # De-code the JSON to instantiate a list of MarketOrder instances that
        # should be identical to self.orderlist.
        decoded_list = unified.parse_from_json(encoded_orderlist)
        self.assertIsInstance(decoded_list, MarketOrderList)
        re_encoded_list = unified.encode_to_json(decoded_list)
        # Re-encode the decoded orderlist. Match the two encoded strings. They
        # should still be the same.
        self.assertEqual(
            encoded_orderlist,
            re_encoded_list,
        )

    def test_history_serialization(self):
        # Encode the sample history instance.
        encoded_history = unified.encode_to_json(self.history)
        # Should return a string JSON representation.
        self.assertIsInstance(encoded_history, basestring)
        # De-code the JSON to instantiate a MarketHistoryList instances that
        # should be identical to self.orderlist.
        decoded_list = unified.parse_from_json(encoded_history)
        self.assertIsInstance(decoded_list, MarketHistoryList)
        re_encoded_history = unified.encode_to_json(decoded_list)
        # Re-encode the decoded history. Match the two encoded strings. They
        # should still be the same.
        self.assertEqual(
            encoded_history,
            re_encoded_history,
        )

class EveMarketeerSerializationTests(BaseSerializationCase):
    """
    Tests for serializing and de-serializing orders in EVE Marketeer format.
    """

    def test_serialization(self):
        pass