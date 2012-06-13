"""
Relays sit below an announcer, or another relay, and simply repeat what
they receive over PUB/SUB.
"""
# Logging has to be configured first before we do anything.
import logging

logger = logging.getLogger(__name__)
import zlib

import gevent
import zmq.green as zmq
from emdr.conf import default_settings as settings
from emdr.daemons.relay.dedupers import is_message_duped

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
        if is_message_duped(message):
            # We've already seen this message recently. Discard it.
            return

        if settings.RELAY_DECOMPRESS_MESSAGES:
            message = zlib.decompress(message)

        sender.send(message)

    logger.info("Relay is now listening for order data.")

    while True:
        # For each incoming message, spawn a greenlet using the relay_worker
        # function.
        gevent.spawn(relay_worker, receiver.recv())