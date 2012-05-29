.. _index:

.. include:: global.txt

EVE Market Data Relay (EMDR)
============================

EVE Market Data Relay is  a super-scalable, super-stable way to accept a large
amount of user-submitted market data (via uploaders), and re-broadcast said
data in near real-time to a large number of subscribers.

The end result is that those writing market-data driven applications can
simply subscribe to a "firehose" of market data, without having
to hassle with writing uploaders, data submission APIs, or scraping data from
other market sites.

For a more complete run-down, see :doc:`overview`.

Learning more
-------------

To learn more about EMDR, see the :doc:`overview`.

**License:** EVE Market Data Relay is licensed under the `BSD License`_.

These links may also be useful to you.

* Source repository: https://github.com/gtaylor/EVE-Market-Data-Relay
* Issue tracker: https://github.com/gtaylor/EVE-Market-Data-Relay/issues
* IRC Room: irc.coldfront.net #emdr
* Mailing list: https://groups.google.com/forum/#!forum/eve-emdr
* Thread on EVE Gate: https://forums.eveonline.com/default.aspx?g=posts&t=95454
* Real-time data monitoring map: http://map.eve-emdr.com/
* @gctaylor on Twitter: https://twitter.com/#!/gctaylor

General Topics
--------------

The following topics are higher-level overviews, and general documentation.
If you are just curious, or wondering how to upload data to EMDR, this section
is all you need.

.. toctree::
   :maxdepth: 2

   overview
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

