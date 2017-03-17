.. _index:

.. include:: global.txt

EVE Market Data Relay (EMDR)
============================

EVE Market Data Relay (EMDR) is a super scalable, highly available firehose of
real-time market data. For those that wish to record price and history data
as it comes in, EMDR will help you do so as efficiently and reliably as
possible. EMDR's data feed is open to the public, and is developed as an
open source project.

EMDR may appeal to you if:

* You need real-time access to market data, as soon as possible. Perhaps for
  sending out price/inventory level alerts, notification of lucrative
  trade routes, or real-time charts and graphs.
* You want to record prices over time.
* You want the absolutely most complete set of data that you can get.
* The effort and overhead of getting large amounts of direct player uploads to
  your site is too much to bear.

EMDR's primary goals are:

* Ensuring that all market sites have access to player-uploaded market data.
* Extremely high reliability.
* Minimize expense to those running EMDR (shared burden).
* Minimize expense to those consuming the feed (bandwidth).

For a more complete run-down, see :doc:`overview`.

**License:** EVE Market Data Relay is licensed under the `BSD License`_.

Assorted Info
-------------
* `Mailing list`_ - If you are consuming the feed, make sure
  to subscribe to this for important announcements. This is also one of the
  best places to ask questions or discuss EMDR stuff.
* Slack Channel - `join #emdr on tweetfleet.slack.com <slack://channel?team=T03CDJ6FV&id=C1L4ZPQAC>`_, an excellent place for getting quick
  help, or hanging out with other developers and consumers. Get your account `here <https://www.fuzzwork.co.uk/tweetfleet-slack-invites/>`_ if you don't have one!
* `Issue tracker`_ - Report bugs here.
* `GitHub project`_ - Source code and issue tracking.
* `EMDR monitor`_ - EMDR relay/announcer monitor web app.
* `EMDR map`_ - See the solar systems light up as
  market data arrives.
* `@gctaylor Twitter`_ - Tweets from the maintainer.

General Topics
--------------

The following topics are higher-level overviews, and general documentation.
If you are just curious, or wondering how to upload data to EMDR, this section
is all you need.

.. toctree::
   :maxdepth: 2

   overview
   sites
   uploading

Consumer Documentation
----------------------

The following topics are useful to those wishing to connect to and use
EMDR's data feed.

.. toctree::
   :maxdepth: 3

   data_sources
   access
   using
   design_considerations

EMDR Developer Documentation
----------------------------

The following topics will be useful to you if you would like to help improve
EMDR, or volunteer additional computing resources to the network.

.. toctree::
   :maxdepth: 2

   installation
   volunteering

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

