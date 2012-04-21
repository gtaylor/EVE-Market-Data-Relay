"""
This module contains the gevent-based Queue and worker that gradually
pushes raw market data out to the worker processes, without blocking the
gateway WSGI app.
"""
import logging
import zlib
import simplejson
import gevent
from gevent.queue import Queue
from gevent_zeromq import zmq
from emdr.conf import default_settings as settings

logger = logging.getLogger(__name__)

# This is the global order queue. The workers all refer to this for the goods.
order_upload_queue = Queue()

# This socket is used to push market data out to worker processes over ZeroMQ.
context = zmq.Context()
sender = context.socket(zmq.PUSH)
# Get the list of transports to bind from settings. This allows us to listen
# for processor connections from multiple places (UNIX sockets + TCP sockets).
# By default, we only listen for UNIX domain sockets.
print("* Order data will be sent to:")
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
        job_dict = order_upload_queue.get()

        try:
            # This will be the representation to send to the processors.
            job_json = simplejson.dumps(job_dict)
        except TypeError:
            logger.error('Unable to serialize a job dict. Discarding.')
            continue

        # Push a zlib compressed JSON representation of the job dict to a
        # processor for a further look.
        compressed_msg = zlib.compress(job_json)
        sender.send(compressed_msg)

# Fire up gevent workers that send raw market order data to processor processes
# in the background without blocking the WSGI app.
print("* Spawning %d PUSH greenlet workers." % settings.NUM_GATEWAY_SENDER_WORKERS)
for worker_num in range(settings.NUM_GATEWAY_SENDER_WORKERS):
    gevent.spawn(worker)
