"""
A memcached-backed deduper. This is much more efficient than the deque backend,
and should be used in production.
"""
import pylibmc
from emdr.conf import default_settings as settings
from emdr.daemons.relay.dedupers.util import calc_hash_for_message

# The connection to memcached.
MC_CLIENT = pylibmc.Client(
    settings.RELAY_DEDUPE_BACKEND_CONN,
    binary=True,
)

def is_message_duped(message):
    """
    Given a raw EMDR message string, determine whether we have already recently
    seen the same exact message.

    :rtype: bool
    :returns: ``True`` if this message is a duplicate, ``False`` if not.
    """
    global MC_CLIENT

    # Generate a hash for the incoming message.
    message_hash = str(calc_hash_for_message(message))
    # Look at our queue of hashes to figure out if we've seen this
    # message yet.
    was_already_seen = MC_CLIENT.get(message_hash) is not None
    # We always push the message on to the queue, even if it ends up being
    # a dupe, since it "refreshes" the hash.
    MC_CLIENT.set(message_hash, 1, time=settings.RELAY_DEDUPE_STORE_TIME)

    return was_already_seen