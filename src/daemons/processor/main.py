"""
The processor daemon PULLs the raw market data from a broker, parses it,
performs some very simple validation, then PUSHes it on to a relay.
"""
# Logging has to be configured first before we do anything.
import logging
from logging.config import dictConfig
import settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('src.daemons.processor.main')

import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
from gevent_zeromq import zmq
from src.daemons.processor import order_processor

# These form the connection to the Gateway daemon(s) upstream.
context = zmq.Context()
receiver = context.socket(zmq.PULL)
# Get the remote gateway binding points from settings. This allows us to add
# additional gateways, which can be local or remote. If multiple bindings are
# specified (IE: local gateway, plus a remote gateway), jobs are routed via
# a fair-queue strategy.
# See: http://api.zeromq.org/2-1:zmq-socket (The ZMQ_PULL section)
for binding in settings.PROCESSOR_RECEIVER_BINDINGS:
    receiver.connect(binding)

sender = context.socket(zmq.PUB)
for binding in settings.RELAY_RECEIVER_BINDINGS:
    sender.connect(binding)

# We use a greenlet pool to cap the number of workers at a reasonable level.
greenlet_pool = Pool(size=settings.NUM_PROCESSOR_WORKERS)

logger.info("Processor daemon started, waiting for jobs...")
logger.info("Worker pool size: %d" % greenlet_pool.size)

while True:
    # Since receiver.recv() blocks when no messages are available, this loop
    # stays under control. If something is available and the greenlet pool
    # has greenlets available for use, work gets done.
    greenlet_pool.spawn(order_processor.worker, receiver.recv(), sender)
