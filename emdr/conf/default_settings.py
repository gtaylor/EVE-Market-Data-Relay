"""
This module contains the default settings that stand unless overridden.
"""

#
## Gateway Daemon Settings
#

# Specifies the number of greenlets to use for sending data to the workers.
NUM_GATEWAY_SENDER_WORKERS = 100
# A list of transports for the gateway to accept connections from. The default
# just allows local socket connections, though you could easily allow local
# UNIX sockets PLUS TCP sockets.
# See: http://api.zeromq.org/2-1:zmq-bind
GATEWAY_SENDER_BINDINGS = ["ipc:///tmp/broker-receiver.sock"]

#
## Broker Daemon Settings
#

BROKER_RECEIVER_BINDINGS = ["ipc:///tmp/broker-receiver.sock"]
BROKER_SENDER_BINDINGS = ["ipc:///tmp/broker-sender.sock"]

#
## Processor Daemon Settings
#

# Specifies the number of greenlets to use for processing raw data from the gateway.
NUM_PROCESSOR_WORKERS = 50
# A list of transports for the processor daemon to connect to. The default
# only connects to the local gateway bound to a UNIX domain socket. You could,
# however, add additional gateways to the list, remote or local.
# See: http://api.zeromq.org/2-1:zmq-connect
PROCESSOR_RECEIVER_BINDINGS = ["ipc:///tmp/broker-sender.sock"]
PROCESSOR_SENDER_BINDINGS = ["ipc:///tmp/announcer-receiver.sock"]

#
## Announcer Daemon Settings
#
ANNOUNCER_RECEIVER_BINDINGS = ["ipc:///tmp/announcer-receiver.sock"]
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
