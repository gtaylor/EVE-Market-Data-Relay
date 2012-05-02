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
