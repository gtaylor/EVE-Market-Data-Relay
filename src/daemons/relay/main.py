"""
There are two kinds of relays, announcer relays, and normal relays. Announcer
relays have a bound socket that processors connect to in order to PUB messages.
The announcer then re-broadcasts the messages to any normal relays beneath it
that are subscribed to the announcer.
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

def start(run_as_announcer=False):
    """
    Fires up the relay process.

    :keyword bool run_as_announcer: If ``True``, this relay will run in
        announcer mode. In announcer mode, the relay accepts connections
        from processor workers, instead of SUBscribing to an upstream relay
        to get its messages.
    """
    if run_as_announcer:
        logger.info("Starting in announcer mode.")
    # These form the connection to the Gateway daemon(s) upstream.
    context = zmq.Context()

    receiver = context.socket(zmq.SUB)
    receiver.setsockopt(zmq.SUBSCRIBE, '')
    for binding in settings.RELAY_RECEIVER_BINDINGS:
        # Relays that are running in 'Announcer' mode have processor workers
        # connecting to PUB messages to. Relays running in normal relay mode
        # connect to an announcer and SUB to them. Announcers are at the root
        # of the relay hierarchy (level 1), whereas normal relays are the
        # branches.
        if run_as_announcer:
            logger.info("Accepting connections from %s" % binding)
            # Processors connect to announcer relays to PUB messages.
            receiver.bind(binding)
        else:
            # Relays connect to an announcer and SUB to get messages.
            logger.info("Subscribing to %s" % binding)
            receiver.connect(binding)

    sender = context.socket(zmq.PUB)
    for binding in settings.RELAY_SENDER_BINDINGS:
        # Regardless of mode, relays always have a ZeroMQ socket that may be
        # connected to in order to get at the data.
        sender.bind(binding)

    def relay_worker(message):
        """
        This is the worker function that re-sends the incoming messages out
        to any subscribers.

        :param str message: A JSON string to re-broadcast.
        """
        print message
        sender.send(message)

    logger.info("Relay is now listening for order data.")

    while True:
        gevent.spawn(relay_worker, receiver.recv())

if __name__ == '__main__':
    start()