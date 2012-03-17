"""
This WSGI application accepts market data uploads from various uploader clients.
The various URLs below are structured to pass off the parsing based on what
format the data is in.

The parsed representation of the order is then sent off to Amazon Simple
Queue Service (SQS), where the worker processes can pull them from for
processing.
"""
from gevent import monkey; monkey.patch_all()
from bottle import run, request, post, default_app

from src.daemons.gateway import parsers
from src.core.market_sqs import enqueue_orders
from src.core.market_data import SerializableOrderList

@post('/api/market-order/upload/eve_marketeer/')
def upload_eve_marketeer():
    """
    This view accepts uploads in EVE Marketeer or EVE Marketdata format. These
    typically arrive via the EVE Unified Uploader client.
    """
    order_list = SerializableOrderList()
    order_generator = parsers.eve_marketeer.parse_from_request(request)
    for order in order_generator:
        order_list.append(order)

    if order_list:
        print "Pushing %d orders." % len(order_list)
        enqueue_orders(order_list)

    return '1'

if __name__ == '__main__':
    # Start the built-in Bottle server for development, for now.
    run(
        host='localhost',
        port=8080,
        server='gevent',
        reloader=True
    )
else:
    application = default_app()