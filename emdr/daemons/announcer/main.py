"""
Announcers are the first daemons to get their mittens on the "finished"
unified format messages. From here, they PUB the messages out to anyone
SUBscribing. This could be Relays, or end-users.
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

    receiver = context.socket(zmq.PULL)
    for binding in settings.ANNOUNCER_RECEIVER_BINDINGS:
        logger.info("Accepting connections from %s" % binding)
        # Processors connect to announcer to PUSH messages.
        receiver.bind(binding)

    sender = context.socket(zmq.PUB)
    for binding in settings.ANNOUNCER_SENDER_BINDINGS:
        # Announcers offer up the data via PUB/SUB.
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