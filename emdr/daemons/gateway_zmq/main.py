"""
This gateway accepts compressed unified uploader format messages over ZMQ.
"""
# Logging has to be configured first before we do anything.
import logging
import zlib
from logging.config import dictConfig
from emdr.conf import default_settings as settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('src.daemons.gateway_zmq.main')

import ujson
import gevent
from gevent import monkey; gevent.monkey.patch_all()
import zmq.green as zmq

from emdr.daemons.gateway.exceptions import MalformedUploadError
from emdr.core.serialization.exceptions import InvalidMarketOrderDataError
from emdr.core.serialization import unified

def start():
    """
    Fires up the announcer process.
    """
    context = zmq.Context()

    receiver = context.socket(zmq.REP)
    for binding in settings.GATEWAY_ZMQ_RECEIVER_BINDINGS:
        logger.info("Accepting connections from %s" % binding)
        receiver.bind(binding)

    sender = context.socket(zmq.PUB)
    for binding in settings.GATEWAY_ZMQ_SENDER_BINDINGS:
        logger.info("Sending data to %s" % binding)
        sender.connect(binding)

    def send_reply(success, message=None):
        """
        Convenience function for sending replies over the receiver socket.

        :param bool success: If ``True``, the message was processed correctly.
            If ``False``, the message failed to process, and an error message
            should be provided.
        :keyword str message: A message describing the failure.
        """
        response_dict = {'success': success, 'message': message}
        compressed_response = zlib.compress(ujson.dumps(response_dict))
        receiver.send(compressed_response)

    def worker():
        """
        This is the worker function that re-sends the incoming messages out
        to any subscribers.

        :param str message: A JSON string to re-broadcast.
        """
        while True:
            message = receiver.recv()

            try:
                decompressed = zlib.decompress(message)
            except zlib.error as exc:
                send_reply(False, message=exc.message)
                return

            try:
                parsed_message = unified.parse_from_json(decompressed)
            except (InvalidMarketOrderDataError, MalformedUploadError) as exc:
                send_reply(False, message=exc.message)
                return

            # All is well.
            send_reply(True)

            # Re-encode the message.
            json_str = unified.encode_to_json(parsed_message)
            # Zlibbify it up.
            compressed_msg = zlib.compress(json_str)
            # Relay to the Announcers.
            sender.send(compressed_msg)

    logger.info("Gateway (ZMQ) is now listening for order data.")
    logger.info("Spawning %d relay workers." % settings.GATEWAY_ZMQ_NUM_WORKERS)

    for worker_num in range(settings.GATEWAY_ZMQ_NUM_WORKERS):
        gevent.spawn(worker())

if __name__ == '__main__':
    start()