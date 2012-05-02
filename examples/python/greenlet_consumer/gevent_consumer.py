#!/usr/bin/env python
"""
An example consumer that uses a greenlet pool to accept incoming market
messages. This example offers a high degree of concurrency.
"""
import zlib
# This can be replaced with the built-in json module, if desired.
import simplejson

import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
import zmq.green as zmq

# The maximum number of greenlet workers in the greenlet pool. This is not one
# per processor, a decent machine can support hundreds or thousands of greenlets.
# I recommend setting this to the maximum number of connections your database
# backend can accept, if you must open one connection per save op.
MAX_NUM_POOL_WORKERS = 200

def main():
    """
    The main flow of the application.
    """
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    # Connect to the first publicly available relay.
    subscriber.connect('tcp://relay-linode-atl-1.eve-emdr.com:8050')
    # Disable filtering.
    subscriber.setsockopt(zmq.SUBSCRIBE, "")

    # We use a greenlet pool to cap the number of workers at a reasonable level.
    greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)

    print("Consumer daemon started, waiting for jobs...")
    print("Worker pool size: %d" % greenlet_pool.size)

    while True:
        # Since subscriber.recv() blocks when no messages are available,
        # this loop stays under control. If something is available and the
        # greenlet pool has greenlets available for use, work gets done.
        greenlet_pool.spawn(worker, subscriber.recv())

def worker(job_json):
    """
    For every incoming message, this worker function is called. Be extremely
    careful not to do anything CPU-intensive here, or you will see blocking.
    Sockets are async under gevent, so those are fair game.
    """
    # Receive raw market JSON strings.
    market_json = zlib.decompress(job_json)
    # Un-serialize the JSON data to a Python dict.
    market_data = simplejson.loads(market_json)
    # Save to your choice of DB here.
    print market_data

if __name__ == '__main__':
    main()

