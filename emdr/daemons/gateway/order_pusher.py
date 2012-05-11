"""
Contains the necessary ZeroMQ socket and a helper function to publish
market data to the Announcer daemons.
"""
import logging
import zlib
import zmq.green as zmq
from emdr.core.serialization import unified
from emdr.conf import default_settings as settings

logger = logging.getLogger(__name__)

# This socket is used to push market data out to the Announcers over ZeroMQ.
context = zmq.Context()
sender = context.socket(zmq.PUB)
# Get the list of transports to bind from settings. This allows us to PUB
# messages to multiple announcers over a variety of socket types
# (UNIX sockets and/or TCP sockets).
for binding in settings.GATEWAY_SENDER_BINDINGS:
    sender.connect(binding)

def push_message(parsed_message):
    """
    Spawned as a greenlet to push parsed messages through ZeroMQ.
    """
    try:
        # This will be the representation to send to the Announcers.
        json_str = unified.encode_to_json(parsed_message)
    except TypeError:
        logger.error('Unable to serialize a parsed message.')
        return

    # Push a zlib compressed JSON representation of the message to
    # announcers.
    compressed_msg = zlib.compress(json_str)
    sender.send(compressed_msg)

