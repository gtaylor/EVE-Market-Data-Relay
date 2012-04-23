"""
This module contains the default settings that stand unless overridden.
"""

#
## Gateway Daemon Settings
#

# Default port to listen for HTTP uploads on.
GATEWAY_WEB_PORT = 8080
# A list of transports for the gateway to accept connections from. The default
# just allows local socket connections, though you could easily allow local
# UNIX sockets PLUS TCP sockets.
# See: http://api.zeromq.org/2-1:zmq-bind
GATEWAY_SENDER_BINDINGS = ["ipc:///tmp/gateway-sender.sock"]

#
## Announcer Daemon Settings
#
ANNOUNCER_RECEIVER_BINDINGS = ["ipc:///tmp/gateway-sender.sock"]
ANNOUNCER_SENDER_BINDINGS = ["ipc:///tmp/announcer-sender.sock"]

#
## Relay Daemon Settings
#
RELAY_RECEIVER_BINDINGS = ["ipc:///tmp/announcer-sender.sock"]
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
