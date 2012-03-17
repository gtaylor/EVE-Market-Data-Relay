"""
This module contains the gevent-based Queue and worker that gradually
pushes market data to SQS without blocking bottle.
"""
import logging
from gevent.queue import Queue

from src.core.market_sqs import enqueue_orders

logger = logging.getLogger(__name__)

# This is the global order queue. The workers all refer to this for the goods.
ORDER_UPLOAD_QUEUE = Queue()

def worker():
    """
    Worker process for the market order pusher. Pushes orders to SQS while
    leaving the WSGI app mostly "un-blocked".
    """
    global ORDER_UPLOAD_QUEUE

    while True:
        # This will block until something arrives in the queue.
        order_list = ORDER_UPLOAD_QUEUE.get()
        # Push the SerializableOrderList (which contains MarketOrder instances)
        # to SQS as a JSON message.
        enqueue_orders(order_list)
        logger.info('Pushed %d orders.' % len(order_list))


