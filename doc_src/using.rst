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

All data coming out of EMDR is in `Unified Uploader Data Interchange Format`_,
which is a JSON-based standard for market orders and history. See the
`spec <Unified Uploader Data Interchange Format>`_ for more details.

Examples for various languages
------------------------------

Below are a few examples of how to connect to the data feed. If you see
anything wrong with the examples below, please let us know on the
`issue tracker`_. The original author of this documentation is only familiar
with Python.

Python
^^^^^^

The following example uses the pyzmq_ module (available off of PyPi)
and simplejson_. For a more complete list of examples, see the
`Python examples`_ dir on github.::

    """
    Example Python EMDR client.
    """
    import zlib
    import zmq
    # You can substitute the stdlib's json module, if that suits your fancy
    import simplejson

    def main():
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)

        # Connect to the first publicly available relay.
        subscriber.connect('tcp://relay-us-central-1.eve-emdr.com:8050')
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
.. _Python examples: https://github.com/gtaylor/EVE-Market-Data-Relay/tree/master/examples/python

PHP
^^^

PHP accesses EMDR via ZeroMQ's `php-zmq`_ PHP bindings:

.. code-block:: php

    <?php
    /*
     * Example PHP EMDR client.
     */

    $context = new ZMQContext();
    $subscriber = $context->getSocket(ZMQ::SOCKET_SUB);

    // Connect to the first publicly available relay.
    $subscriber->connect("tcp://relay-us-central-1.eve-emdr.com:8050");
    // Disable filtering.
    $subscriber->setSockOpt(ZMQ::SOCKOPT_SUBSCRIBE, "");

    while (true) {
        // Receive raw market JSON strings.
    	$market_json = gzuncompress($subscriber->recv());
    	// Un-serialize the JSON data to a named array.
    	$market_data = json_decode($market_json);
    	// Dump the market data to stdout. Or, you know, do more fun things here.
    	var_dump($market_data);
    }

.. _php-zmq: http://www.zeromq.org/bindings:php

Ruby
^^^^

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
    subscriber.connect("tcp://relay-us-central-1.eve-emdr.com:8050")
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
^^

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
                        subscriber.Connect("tcp://relay-us-central-1.eve-emdr.com:8050");

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

Visual Basic
^^^^^^^^^^^^

Visual Basic, like C#, accesses EMDR via ZeroMQ's clrzmq_ binding:

.. code-block:: vb.net

    Imports System.Text
    Imports System.IO
    Imports System.IO.Compression
    Imports System.Web.Script.Serialization ' Needs reference to 'System.Web.Extensions.dll'
    Imports ZMQ ' Needs reference to 'clrzmq.dll' and adding 'libzmq.dll' to project
                ' 'clrzmq' can be found at: https://github.com/zeromq/clrzmq/downloads

    Module MainModule

        Sub Main()
            Using context = New Context()
                Using subscriber = context.Socket(SocketType.SUB)

                    'Connect to the first publicly available relay.
                    subscriber.Connect("tcp://relay-us-central-1.eve-emdr.com:8050")

                    ' Disable filtering.
                    subscriber.SetSockOpt(SocketOpt.SUBSCRIBE, Encoding.UTF8.GetBytes(""))

                    ' Alternatively 'Subscribe' can be used.
                    'subscriber.Subscribe("", Encoding.UTF8)

                    While True
                        Try
                            ' Receive compressed raw market data.
                            Dim receivedData() = subscriber.Recv()

                            ' The following code lines remove the need of 'zlib' usage;
                            ' 'zlib' actually uses the same algorith as 'DeflateStream'.
                            ' To make the data compatible for 'DeflateStream', we only have to remove
                            ' the four last bytes which are the adler32 checksum and
                            ' the two first bytes which are the 'zlib' header.
                            Dim decompressed() As Byte
                            Dim choppedRawData(receivedData.Length - 4) As Byte
                            Array.Copy(receivedData, choppedRawData, choppedRawData.Length)
                            choppedRawData = choppedRawData.Skip(2).ToArray()

                            ' Decompress the raw market data.
                            Using inStream = New MemoryStream(choppedRawData)
                                Using outStream = New MemoryStream()
                                    Dim outZStream = New DeflateStream(inStream, CompressionMode.Decompress)
                                    outZStream.CopyTo(outStream)
                                    decompressed = outStream.ToArray
                                End Using
                            End Using

                            ' Transform data into JSON strings.
                            Dim marketJson = Encoding.UTF8.GetString(decompressed)

                            ' Un-serialize the JSON data to a dictionary.
                            Dim serializer = New JavaScriptSerializer()
                            Dim dictionary = serializer.Deserialize(Of Dictionary(Of String, Object))(marketJson)

                            ' Dump the market data to console or, you know, do more fun things here.
                            For Each pair In dictionary
                                Console.WriteLine("{0}: {1}", pair.Key, pair.Value)
                            Next
                            Console.WriteLine()
                        Catch ex As Exception
                            Console.WriteLine("ZMQ Exception occurred : {0}", ex.Message)
                        End Try
                    End While
                End Using
            End Using
        End Sub
    End Module

Perl
^^^^

Perl uses the `ZeroMQ-Perl`_ binding for Perl:

.. code-block:: perl

    #!/usr/bin/perl
    use warnings;
    use strict;
    $|=1;

    use ZeroMQ qw/:all/;

    my $cxt = ZeroMQ::Context->new;
    my $sock = $cxt->socket(ZMQ_SUB);
    $sock->connect('tcp://relay-us-central-1.eve-emdr.com:8050');
    $sock->setsockopt(ZMQ_SUBSCRIBE, "");

    while (1) {
    	my $msg = $sock->recv();
    	last unless defined $msg;

    	use Compress::Zlib;
    	my $json = uncompress($msg->data);

    	use JSON;
    	my $data = decode_json($json);

    	use Data::Dumper;
    	print Dumper($data),"\n\n";
    }

.. _ZeroMQ-Perl: http://www.zeromq.org/bindings:perl

Java
^^^^

Java uses jzmq_ binding:

.. code-block:: java

    /*
     * Example Java EMDR client.
     */

    import org.zeromq.*; // https://github.com/zeromq/jzmq
    import org.json.simple.*; // http://code.google.com/p/json-simple/downloads/list
    import org.json.simple.parser.*;
    import java.util.zip.*;

    public class EMDR_Client {

        public static void main(String[] args) throws Exception {

            ZMQ.Context context = ZMQ.context(1);
            ZMQ.Socket subscriber = context.socket(ZMQ.SUB);

            // Connect to the first publicly available relay.
            subscriber.connect("tcp://relay-us-central-1.eve-emdr.com:8050");

            // Disable filtering.
            subscriber.subscribe(new byte[0]);

            while (true) {
                try {
                    // Receive compressed raw market data.
                    byte[] receivedData = subscriber.recv(0);

                    // We build a large enough buffer to contain the decompressed data.
                    byte[] decompressed = new byte[receivedData.length * 16];

                    // Decompress the raw market data.
                    Inflater inflater = new Inflater();
                    inflater.setInput(receivedData);
                    int decompressedLength = inflater.inflate(decompressed);
                    inflater.end();

                    byte[] output = new byte[decompressedLength];
                    System.arraycopy(decompressed, 0, output, 0, decompressedLength);

                    // Transform data into JSON strings.
                    String market_json = new String(output, "UTF-8");

                    // Un-serialize the JSON data.
                    JSONParser parser = new JSONParser();
                    JSONObject market_data = (JSONObject)parser.parse(market_json);

                    // Dump the market data to console or, you know, do more fun things here.
                    System.out.println(market_data);
                } catch (ZMQException ex) {
                    System.out.println("ZMQ Exception occurred : " + ex.getMessage());
                }
            }
        }
    }

.. _jzmq: http://www.zeromq.org/bindings:java

Erlang
^^^^^^

Erlang uses erlzmq2_ binding:

.. code-block:: erlang

    #!/usr/bin/env escript

    % you will need the ZeroMQ Erlang library: https://github.com/zeromq/erlzmq2
    % I also use jiffy for Json: https://github.com/davisp/jiffy

    main(_Args) ->
      {ok, Context} = erlzmq:context(),
      {ok, Subscriber} = erlzmq:socket(Context, sub),
      ok = erlzmq:connect(Subscriber,"tcp://relay-us-central-1.eve-emdr.com:8050"),
      ok = erlzmq:setsockopt(Subscriber, subscribe, <<>>),
      msgcheck(Subscriber).

    msgcheck(Subscriber) ->
      {ok,Msg} = erlzmq:recv(Subscriber),
      io:format("~p\n",[jiffy:decode(zlib:uncompress(Msg))]),
      msgcheck(Subscriber).

.. _erlzmq2: https://github.com/zeromq/erlzmq2

Node.js
^^^^^^^

Node.js uses the `zeromq.node`_ binding:

.. code-block:: javascript

    /*
     *  Example node.js EMDR client
     */

    var zmq = require('zmq');
    var zlib = require('zlib');

    var sock = zmq.socket('sub');

    // Connect to the first publicly available relay.
    sock.connect('tcp://relay-us-central-1.eve-emdr.com:8050');
    // Disable filtering
    sock.subscribe('');

    sock.on('message', function(msg){
        // Receive raw market JSON strings.
        zlib.inflate(msg, function(err, market_json) {
            // Un-serialize the JSON data.
            var market_data = JSON.parse(market_json);

            // Do something useful
            console.log(market_data);
        });
    });

.. _zeromq.node: http://www.zeromq.org/bindings:node-js
