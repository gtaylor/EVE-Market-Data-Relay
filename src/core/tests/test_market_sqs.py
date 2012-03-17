import unittest
import datetime
import time

from src.core import market_data
from src.core.market_data import MarketOrder, SerializableOrderList
from src.core.market_sqs import enqueue_orders, pop_orders, reset_sqs_queue
import settings

# Change the queue name so we don't mess with production.
settings.MARKET_ORDER_QUEUE_NAME = 'test-%s' % settings.MARKET_ORDER_QUEUE_NAME

class MarketSQSTests(unittest.TestCase):
    """
    Tests the pushing and popping of lists of MarketOrder instances via
    SerializableOrderList.
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
        )
        self.order2 = MarketOrder(
            order_id=2413387907,
            order_type=market_data.ORDER_TYPE_BUY,
            region_id=10000068,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000069,
            price=500.0,
            volume_entered=5,
            volume_remaining=3,
            minimum_volume=1,
            order_issue_date=datetime.datetime.now(),
            order_duration=90,
            order_range=5,
        )
        self.order_list = SerializableOrderList()
        self.order_list.append(self.order1)
        self.order_list.append(self.order2)

    def test_sqs_queue(self):
        """
        Test the enqueueing and dequeuing of order lists.
        """
        # Start from a clean slate.
        reset_sqs_queue()
        # Enqueues a single order list comprised of the two orders specified
        # in setUp().
        enqueue_orders(self.order_list)

        loop_counter = 0
        while True:
            # SQS entries can take a good while to show up in the queue, so
            # we have to loop for a while until they appear.
            for order_list in pop_orders():
                # Make sure the IDs from the de-coded jobs match the ones
                # that we enqueued.
                if order_list[0].order_id in [self.order1.order_id, self.order2.order_id]:
                    # Match found, we're all good.
                    return True

            # Job hasn't appeared yet
            if loop_counter > 90:
                # Avoid infinite loop. If it hasn't shown up by now, Either
                # AWS is being really slow, or your shit's broke.
                self.fail("Pushed job never came back out.")

            # Prevent SQS request spammage.
            time.sleep(1)
            loop_counter += 1