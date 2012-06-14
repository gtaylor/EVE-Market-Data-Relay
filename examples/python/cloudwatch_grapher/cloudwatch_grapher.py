"""
A simple script that listens to EMDR, tracks the number of messages coming in,
and reports it to Amazon CloudWatch as a custom metric.

CloudWatch allows for nearly real-time graphing from within the AWS Management
Console, and also allows programmatic access to all recorded data. If you
keep the tracking frequency low enough to stay in the free tier (1,000,000
requests per month), this script is free to run.

http://aws.amazon.com/cloudwatch/
"""
import gevent
import gevent.monkey; gevent.monkey.patch_all()
import boto
import zmq.green as zmq

#
## AWS and Route53 config. You MUST replace these.
#

AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

#
## Grapher config
#

# The interval to write to CloudWatch (in seconds). Keeping this high enough
# (no lower than 3 seconds) to stay in the free tier is recommended.
REPORT_INTERVAL = 30

#
## Constants and globals
#

conn = boto.connect_cloudwatch(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

context = zmq.Context()
subscriber = context.socket(zmq.SUB)

# Connect to the first publicly available relay.
subscriber.connect('tcp://relay-us-central-1.eve-emdr.com:8050')
# Disable filtering.
subscriber.setsockopt(zmq.SUBSCRIBE, "")

# This is a global used to track the number of messages we've seen since we
# last reported to CloudWatch.
MESSAGE_COUNTER = 0

#
## The fun stuff
#

def data_sender(num_messages):
    """
    Handles the sending of the message counter values to CloudWatch via boto.
    This is done in a greenlet, and won't block everything else.
    """
    global conn

    conn.put_metric_data('EMDR', 'MessagesOut', value=num_messages, unit='Count')

def heartbeat():
    """
    Every REPORT_INTERVAL number of seconds, this heartbeat greenlet sends
    fires off the data_sender greenlet to report to CloudWatch, and resets
    the message counter.
    """
    global MESSAGE_COUNTER

    while True:
        # Only the greenlet sleeps, everything else (the counter) keeps going.
        gevent.sleep(REPORT_INTERVAL)
        # Fire off another greenlet to send the count to CloudWatch. This lets
        # us immediately get back to sleeping.
        gevent.spawn(data_sender, MESSAGE_COUNTER)
        # Reset the message counter.
        MESSAGE_COUNTER = 0

# Spawns the heartbeat greenlet, which infinitely loops.
gevent.spawn(heartbeat)

def counter_greenlet(message):
    """
    Increments the global message counter by one. This is ran in a greenlet.
    """
    global MESSAGE_COUNTER

    MESSAGE_COUNTER += 1

while True:
    # This is the main driver of the whole script. For every incoming
    # message, hand it off to the counter greenlet, which increments
    # the message counter. We could do also do this here, but doing it in a
    # greenlet is more fun.
    gevent.spawn(counter_greenlet, subscriber.recv())