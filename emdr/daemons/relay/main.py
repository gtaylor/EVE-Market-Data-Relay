"""
Relays sit below an announcer, or another relay, and simply repeat what
they receive over PUB/SUB.
"""
# Logging has to be configured first before we do anything.
import logging
logger = logging.getLogger(__name__)
import zlib
from collections import deque

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

    # Use Python's builtin deque to store a list of hashes for incoming messages.
    hash_queue = deque(maxlen=settings.RELAY_DEDUPE_BUFFER)

    def relay_worker(message):
        """
        This is the worker function that re-sends the incoming messages out
        to any subscribers.

        :param str message: A JSON string to re-broadcast.
        """
        # Generate a hash for the incoming message.
        message_hash = hash(message)
        # Look at our queue of hashes to figure out if we've seen this
        # message yet.
        was_already_seen = message_hash in hash_queue
        # We always push the message on to the queue, even if it ends up being
        # a dupe, since it "refreshes" the hash.
        hash_queue.append(message_hash)

        if settings.RELAY_DEDUPE_BUFFER and was_already_seen:
            # We've already seen this message recently. Discard it.
            return

        if settings.RELAY_DECOMPRESS_MESSAGES:
            message = zlib.decompress(message)

        sender.send(message)
        logger.debug('Message relayed.')

    logger.info("Relay is now listening for order data.")

    while True:
        # For each incoming message, spawn a greenlet using the relay_worker
        # function.
        gevent.spawn(relay_worker, receiver.recv())