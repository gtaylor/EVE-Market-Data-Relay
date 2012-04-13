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

.. warning:: The hostnames you see below may change. We are currently in
    testing, so anything you see now is considered non-final.

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
        subscriber.connect('tcp://relay-linode-atl-1.eve-emdr.com:8050')
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

PHP accesses EMDR via ZeroMQ's `php-zmq`_ PHP bindings:

.. code-block:: php

    <?php
    /*
     * Example PHP EMDR client.
     */

    $context = new ZMQContext();
    $subscriber = $context->getSocket(ZMQ::SOCKET_SUB);

    // Connect to the first publicly available relay.
    $subscriber->connect("tcp://relay-linode-atl-1.eve-emdr.com:8050");
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

Ruby accesses EMDR via ZeroMQ's zmq_ Ruby bindings:

.. code-block:: ruby

    #
    # Synchronized subscriber
    #

    require 'rubygems'
    require 'ffi-rzmq'
    require 'json'
    require 'zlib'

    context = ZMQ::Context.new
    subscriber = context.socket(ZMQ::SUB)

    // Connect to the first publicly available relay.
    subscriber.connect("tcp://relay-linode-atl-1.eve-emdr.com:8050")
    subscriber.setsockopt(ZMQ::SUBSCRIBE,"")

    loop do
      // Receive raw market JSON strings.
      subscriber.recv_string(string = '')
      // Un-compress the stream.
      market_json = Zlib::Inflate.new(Zlib::MAX_WBITS).inflate(string)
      // Un-serialize the JSON data.
      market_data = JSON.parse(market_json)
      // Dump the market data to stdout. Or, you know, do more fun things here.
      puts market_data
    end

.. _zmq: http://www.zeromq.org/bindings:ruby
