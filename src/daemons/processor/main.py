"""
The processor daemon accepts the raw market data, parses it, performs some
very simple validation, then passes it on to the relay.
"""
# Logging has to be configured first before we do anything.
import logging
from logging.config import dictConfig
import settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('src.daemons.gateway.wsgi')

import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
from gevent_zeromq import zmq

from src.daemons.processor import order_processor

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("ipc:///tmp/order-publisher.sock")

# We use a greenlet pool to cap the number of workers at a reasonable level.
greenlet_pool = Pool(size=settings.NUM_PROCESSOR_WORKERS)

while True:
    # Since receiver.recv() blocks when no messages are available, this loop
    # stays under control. If something is available and the greenlet pool
    # has greenlets available for use, work gets done.
    greenlet_pool.spawn(order_processor.worker, receiver.recv())
