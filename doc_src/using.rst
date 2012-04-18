.. _using:

.. include:: global.txt

Connecting to the EMDR network
==============================

In order to connect to the EVE Market Data Relay feed, you'll need to use
the ZeroMQ_ bindings for the language of your choice. This involves installing
ZeroMQ_, then installing the bindings. See your language's section below for
a link to its bindings.

Once you have ZeroMQ_ plus bindings installed, you'll need to choose a
Relay to connect to. See :doc:`access` for a list, and any potential special
case instructions for each relay. After that, you'll be set to connect and
begin receiving data.

Data Format
-----------

All data coming out of EMDR is in `Unified Uploader Interchange Format`_,
which is a JSON-based standard for market orders and history. See the
`spec <Unified Uploader Interchange Format>`_ for more details.

Examples for various languages
------------------------------

Below are a few examples of how to connect to the data feed. If you see
anything wrong with the examples below, please let us know on the
`issue tracker`_. The original author of this documentation is only familiar
with Python.

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

C#
--

C# accesses EMDR via ZeroMQ's clrzmq_ binding:

.. code-block:: c#

    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.IO.Compression;
    using System.Linq;
    using System.Text;
    using System.Web.Script.Serialization; // Needs reference to 'System.Web.Extensions.dll'
    using ZMQ; // Needs reference to 'clrzmq.dll' and adding 'libzmq.dll' to project
               // 'clrzmq' can be found at: https://github.com/zeromq/clrzmq/downloads

    namespace EMDR_Client
    {
        public class Program
        {
            private static void Main()
            {
                using (var context = new Context())
                {
                    using (var subscriber = context.Socket(SocketType.SUB))
                    {
                        //Connect to the first publicly available relay.
                        subscriber.Connect("tcp://relay-linode-atl-1.eve-emdr.com:8050");

                        // Disable filtering.
                        subscriber.SetSockOpt(SocketOpt.SUBSCRIBE, Encoding.UTF8.GetBytes(""));

                        // Alternatively 'Subscribe' can be used
                        //subscriber.Subscribe("", Encoding.UTF8);

                        while (true)
                        {
                            try
                            {
                                // Receive compressed raw market data.
                                var receivedData = subscriber.Recv();

                                // The following code lines remove the need of 'zlib' usage;
                                // 'zlib' actually uses the same algorith as 'DeflateStream'.
                                // To make the data compatible for 'DeflateStream', we only have to remove
                                // the four last bytes which are the adler32 checksum and
                                // the two first bytes which are the 'zlib' header.
                                byte[] decompressed;
                                byte[] choppedRawData = new byte[(receivedData.Length - 4)];
                                Array.Copy(receivedData, choppedRawData, choppedRawData.Length);
                                choppedRawData = choppedRawData.Skip(2).ToArray();

                                // Decompress the raw market data.
                                using (MemoryStream inStream = new MemoryStream(choppedRawData))
                                using (MemoryStream outStream = new MemoryStream())
                                {
                                    DeflateStream outZStream = new DeflateStream(inStream, CompressionMode.Decompress);
                                    outZStream.CopyTo(outStream);
                                    decompressed = outStream.ToArray();
                                }

                                // Transform data into JSON strings.
                                string marketJson = Encoding.UTF8.GetString(decompressed);

                                // Un-serialize the JSON data to a dictionary.
                                var serializer = new JavaScriptSerializer();
                                var dictionary = serializer.Deserialize<Dictionary<string, object>>(marketJson);

                                // Dump the market data to console or, you know, do more fun things here.
                                foreach (KeyValuePair<string, object> pair in dictionary)
                                {
                                    Console.WriteLine("{0}: {1}", pair.Key, pair.Value);
                                }
                                Console.WriteLine();
                            }
                            catch (ZMQ.Exception ex)
                            {
                                Console.WriteLine("ZMQ Exception occurred : {0}", ex.Message);
                            }
                        }
                    }
                }
            }
        }
    }

.. _clrzmq: https://github.com/zeromq/clrzmq/downloads