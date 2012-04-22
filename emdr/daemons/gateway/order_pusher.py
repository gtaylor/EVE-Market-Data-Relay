"""
This module contains the gevent-based Queue and worker that gradually
pushes parsed market data (in Unified Uploader Interchange format)
out to the Announcers over PUB, without blocking the gateway WSGI app.
"""
import logging
import zlib
import gevent
from gevent.queue import Queue
from gevent_zeromq import zmq
from emdr.core.serialization import unified
from emdr.conf import default_settings as settings

logger = logging.getLogger(__name__)

# This is the global order queue. The workers all refer to this for the goods.
order_upload_queue = Queue()

# This socket is used to push market data out to the Announcers over ZeroMQ.
context = zmq.Context()
sender = context.socket(zmq.PUB)
# Get the list of transports to bind from settings. This allows us to PUB
# messages to multiple announcers over a variety of socket types
# (UNIX sockets and/or TCP sockets).
print("* Market message data will be sent to:")
for binding in settings.GATEWAY_SENDER_BINDINGS:
    print("   - %s" % binding)
    sender.connect(binding)

def worker():
    """
    Worker process for the market order pusher. Pushes orders to SQS while
    leaving the WSGI app mostly "un-blocked".
    """
    while True:
        # This will block until something arrives in the queue.
        parsed_message = order_upload_queue.get()

        try:
            # This will be the representation to send to the processors.
            json_str = unified.encode_to_json(parsed_message)
        except TypeError:
            logger.error('Unable to serialize a parsed message.')
            continue

        # Push a zlib compressed JSON representation of the message to
        # announcers.
        compressed_msg = zlib.compress(json_str)
        sender.send(compressed_msg)

# Fire up gevent workers that send raw market order data to processor processes
# in the background without blocking the WSGI app.
print("* Spawning %d PUSH greenlet workers." % settings.NUM_GATEWAY_SENDER_WORKERS)
for worker_num in range(settings.NUM_GATEWAY_SENDER_WORKERS):
    gevent.spawn(worker)
