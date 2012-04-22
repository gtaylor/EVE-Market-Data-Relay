.. _design-considerations:

.. include:: global.txt

Design considerations for consumers
===================================

This document outlines some useful tips in designing your consumer applications.
If you have anything to add, post an entry on our `issue tracker`_.

Keeping up with market data
---------------------------

As EMDR grows, the volume of market data you see over a given span of time
will continue to increase. This means that you'll need to design with
concurrency in mind.

Ideally, you have a dedicated process that is just enough to connect to EMDR
and save the data to your DB backend. We suggest doing any aggregation or
additional processing in another process, to make sure you don't lose any
data due to blocking or bugs introduced in your processing/aggregation code.

For an idea of what this looks like, see our greenlet_consumer_ code example.
This is written in Python, using gevent_ to perform the DB saves using
greenlets, which are micro-threads. Most languages have something similar
available, so don't let the fact that this is in Python psyche you out if you're
using another language.

.. _greenlet_consumer: https://github.com/gtaylor/EVE-Market-Data-Relay/blob/master/examples/python/greenlet_consumer/gevent_consumer.py

Deal with duplicate data
------------------------

You will see some duplicate data coming down through EMDR. There are a few
different kinds of duplication:

* Multiple players are sitting in Jita, looking at Module X at about the same
  time. You'll see two individual messages, containing the same (or very similar)
  data.
* Another market service uploads a message that has already been through EMDR.
  This is a duplicate in its purest sense. We will do our best to hunt this
  down and take care of it for you, but do design with it in mind.

Some elect to store every individual data point for each item. This is a
viable approach, and not extremely expensive. Your aggregator process can
go through data as it's coming in to look for suspicious patterns. Duplicate
data can be a valuable means of cross-checking incoming data, in this case.

Others only store the current price for items, using the generatedAt values
to determine whether the message contains newer data than they have.

Don't be too trusting
---------------------

The reality of player-upload-driven market data sites is that we are at the
mercy of said players as far as the data goes. The vast majority of uploaders
are going to send good data. However, there is a minority that does not play
so nicely.

In many cases, multiple players will upload the details for the same orders
multiple times. This can be used to your advantage, in that you can cross-check
things as they come in. If one message says Large Shield Extender I is going
for 5 billion isk in Jita, but another three are saying much lower than that,
your outlier is probably fraudulent and is best ignored.

You also have the option of cross-referencing the APIs of other sites who
do not consume EMDR data. While this can defeat some of the purpose of using
EMDR, the option is there to complement the feed.