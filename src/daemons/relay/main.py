"""
The relay PULLs from the workers, then PUBs to the consumers.
"""
# Logging has to be configured first before we do anything.
import logging
from logging.config import dictConfig
import settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('src.daemons.relay.main')

import gevent
from gevent import monkey; gevent.monkey.patch_all()
from gevent_zeromq import zmq

# These form the connection to the Gateway daemon(s) upstream.
context = zmq.Context()

receiver = context.socket(zmq.PULL)
for binding in settings.RELAY_RECEIVER_BINDINGS:
    receiver.bind(binding)

sender = context.socket(zmq.PUB)
for binding in settings.RELAY_SENDER_BINDINGS:
    sender.bind(binding)

def relay_worker(message):
    print message
    sender.send(message)

while True:
    gevent.spawn(relay_worker, receiver.recv())
