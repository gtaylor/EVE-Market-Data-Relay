"""
This module contains the default settings that stand unless overridden.
"""
# Amazon Web Services credentials.
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None

# The name of the SQS queue that holds incoming orders waiting for an economist.
MARKET_ORDER_QUEUE_NAME = 'incoming-orders'
# If an economist grabs the order from the queue, but doesn't signify that
# it has been processed in this number of seconds, the order re-appears in
# the queue to get another shot at being processed.
MARKET_ORDER_QUEUE_VIS_TIMEOUT = 60 * 10