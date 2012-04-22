"""
Gateways connect to Announcer daemons, sending zlib compressed JSON
representations of market data. From here, the Announcer PUBs the messages
out to anyone SUBscribing. This could be Relays, or end-users.
"""
# Logging has to be configured first before we do anything.
import logging
from logging.config import dictConfig
from emdr.conf import default_settings as settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('src.daemons.announcer.main')

import gevent
from gevent import monkey; gevent.monkey.patch_all()
from gevent_zeromq import zmq

def start():
    """
    Fires up the announcer process.
    """
    context = zmq.Context()

    receiver = context.socket(zmq.SUB)
    receiver.setsockopt(zmq.SUBSCRIBE, '')
    for binding in settings.ANNOUNCER_RECEIVER_BINDINGS:
        logger.info("Accepting connections from %s" % binding)
        # Gateways connect to the Announcer to PUB messages.
        receiver.bind(binding)

    sender = context.socket(zmq.PUB)
    for binding in settings.ANNOUNCER_SENDER_BINDINGS:
        # Announcers offer up the data via PUB.
        sender.bind(binding)

    def relay_worker(message):
        """
        This is the worker function that re-sends the incoming messages out
        to any subscribers.

        :param str message: A JSON string to re-broadcast.
        """
        sender.send(message)

    logger.info("Announcer is now listening for order data.")

    while True:
        gevent.spawn(relay_worker, receiver.recv())

if __name__ == '__main__':
    start()