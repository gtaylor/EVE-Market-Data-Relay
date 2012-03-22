"""
The broker PULLs from gateways and PUSHes to processors. Running a broker is
completely optional, but may make it easier to add redundancy.
"""
# Logging has to be configured first before we do anything.
import logging
from logging.config import dictConfig
import settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('src.daemons.broker.main')

import gevent
from gevent import monkey; gevent.monkey.patch_all()
from gevent_zeromq import zmq

# These form the connection to the Gateway daemon(s) upstream.
context = zmq.Context()

receiver = context.socket(zmq.PULL)
# See: http://api.zeromq.org/2-1:zmq-socket (The ZMQ_PULL section)
for binding in settings.BROKER_RECEIVER_BINDINGS:
    receiver.bind(binding)

sender = context.socket(zmq.PUSH)
for binding in settings.BROKER_SENDER_BINDINGS:
    sender.bind(binding)

def broker_worker(message):
    logger.info("Doling out a task to worker.")
    sender.send(message)

logger.info("Broker startup complete, waiting for orders...")
while True:
    gevent.spawn(broker_worker, receiver.recv())
