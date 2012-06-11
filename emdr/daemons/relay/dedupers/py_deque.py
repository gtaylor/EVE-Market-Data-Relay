"""
A simple, inefficient de-duper using Python's included deque data structure.
Seek time is pretty high, so this is probably only best for developers.
"""
from collections import deque
from emdr.daemons.relay.dedupers.util import calc_hash_for_message

# A simple Python deque. See the docs for details on how this works:
# http://docs.python.org/library/collections.html#collections.deque
# We hardcode this, because it's mostly meant for testing when memcached
# isn't available.
HASH_DEQUE = deque(maxlen=500)

def is_message_duped(message):
    """
    Given a raw EMDR message string, determine whether we have already recently
    seen the same exact message.

    :rtype: bool
    :returns: ``True`` if this message is a duplicate, ``False`` if not.
    """
    global HASH_DEQUE

    # Generate a hash for the incoming message.
    message_hash = calc_hash_for_message(message)
    # Look at our queue of hashes to figure out if we've seen this
    # message yet.
    was_already_seen = message_hash in HASH_DEQUE
    # We always push the message on to the queue, even if it ends up being
    # a dupe, since it "refreshes" the hash.
    HASH_DEQUE.append(message_hash)

    return was_already_seen