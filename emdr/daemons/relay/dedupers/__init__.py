"""
This module contains a few simple message de-duplication backends. These are
used to de-dupe messages, since relays will be connected to at least two
upstream announcers/relays.
"""
from emdr.conf import default_settings as settings

if settings.RELAY_DEDUPE_BACKEND == 'memcached':
    # Memcached backend. This is currently the fastest.
    #noinspection PyUnresolvedReferences
    from emdr.daemons.relay.dedupers.memcached import is_message_duped
elif settings.RELAY_DEDUPE_BACKEND == 'deque':
    # Default to the included deque.
    #noinspection PyUnresolvedReferences
    from emdr.daemons.relay.dedupers.py_deque import is_message_duped
else:
    raise Exception("Unknown deduplication backend.")