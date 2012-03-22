"""
This WSGI application accepts market data uploads from various uploader clients.
The various URLs below are structured to pass off the parsing based on what
format the data is in.

The parsed representation of the order is then sent off to the processor nodes,
where the data is parsed, some light validation is performed, then passed off
to the relay for re-broadcasting to consumers.
"""
# Logging has to be configured first before we do anything.
import logging
from logging.config import dictConfig
import settings
dictConfig(settings.LOGGING)
logger = logging.getLogger('src.daemons.gateway.wsgi')

import gevent
from gevent import monkey; gevent.monkey.patch_all()
#noinspection PyUnresolvedReferences
from bottle import run, request, post, default_app

from src.core.market_data import SerializableOrderList
from src.daemons.gateway import parsers
from src.daemons.gateway import order_pusher

@post('/api/market-order/upload/eve_marketeer/')
def upload_eve_marketeer():
    """
    This view accepts uploads in EVE Marketeer or EVE Marketdata format. These
    typically arrive via the EVE Unified Uploader client.
    """
    # Orders are lumped into this list sub-class, which has JSON-serialization
    # methods on it.
    order_list = SerializableOrderList()

    # This generator spits out the MarketOrder instances the user sent.
    order_generator = parsers.eve_marketeer.parse_from_request(request)
    for order in order_generator:
        order_list.append(order)

    if order_list:
        # Send the entire list of orders that came in this request to a gevent
        # queue, where they'll await pushing to an Amazon SQS queue.
        order_pusher.order_upload_queue.put(order_list)

    # Goofy, but apparently expected by EVE Market Data Uploader.
    return '1'

# Fire up gevent workers that send raw market order data to processor processes
# in the background without blocking the WSGI app.
for worker_num in range(settings.NUM_GATEWAY_SENDER_WORKERS):
    logger.info("Spawning Gateway->Processor PUSH worker.")
    gevent.spawn(order_pusher.worker)

if __name__ == '__main__':
    # Start the built-in Bottle server for development, for now.
    run(
        host='localhost',
        port=8080,
        server='gevent',
    )
else:
    # gunicorn will eventually use this in production.
    application = default_app()