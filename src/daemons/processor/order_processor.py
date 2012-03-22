"""
The worker function in this module performs the order processing.
"""
import logging

logger = logging.getLogger(__name__)

def worker(order_data, sender):
    """
    TODO: Make this useful.
    """
    logger.info('Processing one job.')
    sender.send(order_data)
