"""
This module contains the default settings that stand unless overridden.
"""

#
## Gateway Daemon Settings
#

# Default port to listen for HTTP uploads on.
GATEWAY_WEB_PORT = 8080
# PUB - Connect
GATEWAY_SENDER_BINDINGS = ["ipc:///tmp/announcer-receiver.sock"]
# If set as a string, this value is used as the salt to create a hash of
# each uploader's IP address. This in turn gets set as the EMDR upload key.
GATEWAY_IP_KEY_SALT = None

#
## ZeroMQ-based Gateway Daemon Settings
#
# PULL - Bind
GATEWAY_ZMQ_RECEIVER_BINDINGS = ["ipc:///tmp/gateway-zmq-receiver.sock"]
# By default, use the same as the HTTP gateway, for easy testing.
# PUB - Connect
GATEWAY_ZMQ_SENDER_BINDINGS = ["ipc:///tmp/announcer-receiver.sock"]
# The number of worker greenlets to listen for data on.
GATEWAY_ZMQ_NUM_WORKERS = 5

#
## Announcer Daemon Settings
#
# SUB - Bind
ANNOUNCER_RECEIVER_BINDINGS = ["ipc:///tmp/announcer-receiver.sock"]
# PUB - Bind
ANNOUNCER_SENDER_BINDINGS = ["ipc:///tmp/announcer-sender.sock"]

#
## Relay Daemon Settings
#
# SUB - Connect
RELAY_RECEIVER_BINDINGS = ["ipc:///tmp/announcer-sender.sock"]
# PUB - Bind
RELAY_SENDER_BINDINGS = ["ipc:///tmp/relay-sender.sock"]
# If True, outbound messages to subscribers are decompressed.
RELAY_DECOMPRESS_MESSAGES = False
# Default to memcached, as it's fast.
RELAY_DEDUPE_BACKEND = "memcached"
# For dedupe backends that require a connection string of some sort, store it
# here. We'll default to localhost for now. Use a list of strings.
RELAY_DEDUPE_BACKEND_CONN = ["127.0.0.1"]
# For timeout based backends, this determines how long (in seconds) we store
# the message hashes.
RELAY_DEDUPE_STORE_TIME = 300
# For memcached and other key/value stores, this is prefixed to the hash
# to form the cache key. This is useful to avoid clashes for multi-tenant
# situations.
RELAY_DEDUPE_STORE_KEY_PREFIX = 'emdr-relay-dd'

#
## Logging Settings
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(name)s -- %(levelname)s -- %(asctime)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
