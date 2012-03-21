"""
This module contains the gevent-based Queue and worker that gradually
pushes raw market data out to the worker processes, without blocking the
gateway WSGI app.
"""
import logging
from gevent.queue import Queue
from gevent_zeromq import zmq

logger = logging.getLogger(__name__)

# This is the global order queue. The workers all refer to this for the goods.
ORDER_UPLOAD_QUEUE = Queue()

# This socket is used to push market data out to worker processes over ZeroMQ.
ZMQ_CONTEXT = zmq.Context()
ORDER_SENDER = ZMQ_CONTEXT.socket(zmq.PUSH)
ORDER_SENDER.bind("ipc:///tmp/order-publisher.sock")

def worker():
    """
    Worker process for the market order pusher. Pushes orders to SQS while
    leaving the WSGI app mostly "un-blocked".
    """
    global ORDER_PUBLISHER

    while True:
        # This will block until something arrives in the queue.
        order_list = ORDER_UPLOAD_QUEUE.get()

        # Push the SerializableOrderList (which contains MarketOrder instances)
        # to SQS as a JSON message.
        ORDER_SENDER.send(order_list.to_json())
        logger.info('Pushed %d orders.' % len(order_list))


