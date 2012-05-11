"""
This gateway accepts compressed unified uploader format messages over ZMQ.
"""
import logging
import zlib
logger = logging.getLogger(__name__)

import ujson
import gevent
import zmq.green as zmq

from emdr.conf import default_settings as settings
from emdr.daemons.gateway.exceptions import MalformedUploadError
from emdr.core.serialization.exceptions import InvalidMarketOrderDataError
from emdr.core.serialization import unified

def run():
    """
    Fires up the gateway-zmq process.
    """
    context = zmq.Context()

    receiver = context.socket(zmq.REP)
    for binding in settings.GATEWAY_ZMQ_RECEIVER_BINDINGS:
        receiver.bind(binding)

    sender = context.socket(zmq.PUB)
    for binding in settings.GATEWAY_ZMQ_SENDER_BINDINGS:
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

    def get_decompressed_message(message):
        """
        De-compresses the incoming message using zlib. Attempts several
        different decompression methods, ending with the most permissive one.

        :rtype: str
        :returns: The de-compressed message JSON string.
        :raises: zlib.error if decompression fails for all of our attempts.
        """
        try:
            return zlib.decompress(message)
        except zlib.error:
            # The default decompression method failed, let's fall through to
            # another approach.
            pass

        # If this succeeds, great, return. If not, let the zlib.error get
        # passed up to the invoking worker.
        return zlib.decompress(message, -15)

    def worker():
        """
        This is the worker function that re-sends the incoming messages out
        to any subscribers.
        """
        while True:
            message = receiver.recv()

            try:
                decompressed = get_decompressed_message(message)
            except zlib.error as exc:
                send_reply(False, message=exc.message)
                continue

            try:
                parsed_message = unified.parse_from_json(decompressed)
            except (InvalidMarketOrderDataError, MalformedUploadError) as exc:
                send_reply(False, message=exc.message)
                continue

            # All is well.
            send_reply(True)

            # Re-encode the message.
            json_str = unified.encode_to_json(parsed_message)
            # Zlibbify it up.
            compressed_msg = zlib.compress(json_str)
            # Relay to the Announcers.
            sender.send(compressed_msg)

            logger.info("Accepted Unified %s upload from ?" % (
                parsed_message.result_type,
            ))

    for worker_num in range(settings.GATEWAY_ZMQ_NUM_WORKERS):
        gevent.spawn(worker())

    logger.info("Gateway (ZMQ) is now listening for order data.")