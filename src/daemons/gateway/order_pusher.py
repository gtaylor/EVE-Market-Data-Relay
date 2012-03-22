"""
This module contains the gevent-based Queue and worker that gradually
pushes raw market data out to the worker processes, without blocking the
gateway WSGI app.
"""
import logging
from gevent.queue import Queue
from gevent_zeromq import zmq
import settings

logger = logging.getLogger(__name__)

# This is the global order queue. The workers all refer to this for the goods.
order_upload_queue = Queue()

# This socket is used to push market data out to worker processes over ZeroMQ.
context = zmq.Context()
sender = context.socket(zmq.PUSH)
# Get the list of transports to bind from settings. This allows us to listen
# for processor connections from multiple places (UNIX sockets + TCP sockets).
# By default, we only listen for UNIX domain sockets.
for binding in settings.GATEWAY_SENDER_BINDINGS:
    sender.connect(binding)

def worker():
    """
    Worker process for the market order pusher. Pushes orders to SQS while
    leaving the WSGI app mostly "un-blocked".
    """
    while True:
        # This will block until something arrives in the queue.
        order_list = order_upload_queue.get()

        # Push the SerializableOrderList (which contains MarketOrder instances)
        # to SQS as a JSON message.
        sender.send(order_list.to_json())
        logger.info('Pushed %d orders.' % len(order_list))


