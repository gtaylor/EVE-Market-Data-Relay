.. _using:

.. include:: global.txt

Using data from the EMDR network
================================

All data coming out of EMDR is in `Unified Uploader Interchange Format`_,
which is a JSON-based standard for market orders and history. See the
`spec <Unified Uploader Interchange Format>`_ for more details.

Below are a few examples of how to connect to the data feed. If you see
anything wrong with the examples below, please let us know on the
`issue tracker`_. The original author of this documentation is only familiar
with Python.

.. warning:: Right now, the hostnames you see below are not in action. They
    will become active once we complete our first deployment.

.. _Unified Uploader Interchange Format: http://dev.eve-central.com/unifieduploader/start

Python
------

The following example uses the pyzmq_ module (available off of PyPi)
and simplejson_. You can substitute the stdlib's json_ module, if that suits
your fancy::

    #
    #  Example Python EMDR client.
    #
    import zlib
    import zmq
    import simplejson

    def main():
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)

        # Connect to the first publicly available relay.
        subscriber.connect('tcp://relay1.eve-emdr.com:5561')
        # Disable filtering.
        subscriber.setsockopt(zmq.SUBSCRIBE, "")

        while True:
            # Receive raw market JSON strings.
            market_json = zlib.decompress(subscriber.recv())
            # Un-serialize the JSON data to a Python dict.
            market_data = simplejson.loads(market_json)
            # Dump the market data to stdout. Or, you know, do more fun
            # things here.
            print market_data

    if __name__ == '__main__':
        main()

.. _pyzmq: http://pypi.python.org/pypi/pyzmq/
.. _simplejson: http://pypi.python.org/pypi/simplejson/
.. _json: http://docs.python.org/library/json.html

PHP
---

PHP accesses EMDR via ZeroMQ's `php-zmq`_ PHP bindings::

    <?php
    /*
     * Example PHP EMDR client.
     */

    $context = new ZMQContext();
    $subscriber = $context->getSocket(ZMQ::SOCKET_SUB);

    // Connect to the first publicly available relay.
    $subscriber->connect("tcp://relay1.eve-emdr.com:5561");
    // Disable filtering.
    $subscriber->setSockOpt(ZMQ::SOCKOPT_SUBSCRIBE, "");

    while (true) {
        // Receive raw market JSON strings.
    	$market_json = gzuncompress($subscriber->recv());
    	// Un-serialize the JSON data to a named array.
    	$market_data = json_decode($market_json);
    	// Dump the market data to stdout. Or, you know, do more fun things here.
    	printf($market_data);
    }

.. _php-zmq: http://www.zeromq.org/bindings:php

Ruby
----

Ruby accesses EMDR via ZeroMQ's zmq_ Ruby bindings::

    #
    # Synchronized subscriber
    #

    require 'rubygems'
    require 'ffi-rzmq'

    context = ZMQ::Context.new
    subscriber = context.socket(ZMQ::SUB)

    // Connect to the first publicly available relay.
    subscriber.connect("tcp://relay1.eve-emdr.com:5561")
    subscriber.setsockopt(ZMQ::SUBSCRIBE,"")

    loop do
      subscriber.recv_string(string = '')
      # I'm not sure how zlib works with Ruby, but you'll need to
      # Zlib.decompress(), which will leave you with a JSON string. You
      # can then decode the JSON to leave yourself with a Ruby dict, or
      # whatever they're called. If you don't at least decompress this with
      # Zlib, you're going to see lots of gibberish.
      puts string
    end

.. note:: If anyone would like to contribute the correct code for this
    Ruby example, please post on our `issue tracker`_.

.. _zmq: http://www.zeromq.org/bindings:ruby