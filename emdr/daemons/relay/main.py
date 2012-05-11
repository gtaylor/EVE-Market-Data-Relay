"""
Relays sit below an announcer, or another relay, and simply repeat what
they receive over PUB/SUB.
"""
# Logging has to be configured first before we do anything.
import logging
logger = logging.getLogger(__name__)

import gevent
import zmq.green as zmq
from emdr.conf import default_settings as settings

def run():
    """
    Fires up the relay process.
    """
    # These form the connection to the Gateway daemon(s) upstream.
    context = zmq.Context()

    receiver = context.socket(zmq.SUB)
    receiver.setsockopt(zmq.SUBSCRIBE, '')
    for binding in settings.RELAY_RECEIVER_BINDINGS:
        # Relays bind upstream to an Announcer, or another Relay.
        receiver.connect(binding)

    sender = context.socket(zmq.PUB)
    for binding in settings.RELAY_SENDER_BINDINGS:
        # End users, or other relays, may attach here.
        sender.bind(binding)

    def relay_worker(message):
        """
        This is the worker function that re-sends the incoming messages out
        to any subscribers.

        :param str message: A JSON string to re-broadcast.
        """
        #import zlib
        #print zlib.decompress(message)
        sender.send(message)
        logger.debug('Message relayed.')

    logger.info("Relay is now listening for order data.")

    while True:
        gevent.spawn(relay_worker, receiver.recv())