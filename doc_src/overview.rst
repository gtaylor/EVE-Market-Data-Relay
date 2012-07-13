.. _overview:

.. include:: global.txt

A High-Level Overview
=====================

Project Motivation
------------------

**For the application developer**, there are quite a few
barriers to entry for those wishing to write market-data-driven applications.
A developer would probably need to:

* Either write their own uploader client, or re-purpose an existing uploader.
* Write a service/API to accept the data in whatever format(s) the uploader(s)
  they'd like to support use.
* Actually get players to point their uploader at said service/API (This is the
  hardest part!)
* Probably pull data from other market sites to flesh out their data set.
* Then, and only then, start writing the *fun* part of their application as
  the amount of data coming in slowly grows. By this point, they are probably
  a ways down the road to burnout.

None of these tasks are fun, they all involve re-inventing the wheel. By the
time the developer gets through all of this (if they do), burnout is a distinct
possibility. All before getting to the fun stuff!

EVE Market Data Relay (EMDR) allows you to forgo all of this drudgery, and
instead, connect to a firehose of data in the standardized
`Unified Uploader Data Interchange Format`_ format. EMDR's ZeroMQ_ underpinnings also
make it easier, and exponentially more efficient than accepting HTTP
uploads directly.

Core Principles
---------------

During the early design and development of EMDR, these were the main pillars
we built on:

* There should be no single point of failure. Every component of the
  architecture should be simple to make redundant using trusted volunteered
  machines.
* The application must be able to accept an extremely large number of incoming
  market orders without performance issues.
* The cost for people hosting parts of EMDR's network should be kept to an
  absolute minimum. This means being stingey with CPU, RAM, and bandwidth.
  Likewise, consuming the feed shouldn't break the bank, either.
* It must be very easy to scale the system without restarts/reconfigs on the
  primary setup.
* The broadcasting of the market data needs to happen in a "fan out" manner.
  In this way, we can keep adding additional subscribers without running into
  scalability issues.

How it all fits together
------------------------

For any given submitted market order, here is the flow said order goes through::

    (Gateway) -> (Announcer) -> (Relays) -> (Applications)

First, the order hits the **Gateway**, which is a simple HTTP application
that parses the message. Incoming messages are in
`Unified Uploader Data Interchange Format`_.

The Gateway interprets the message, validates it, normalizes anything weird,
then pipes it to all of the root-level **Announcers** in the network.

The **Announcer** is the first tier of our market data distribution.
Announcers relay any data they receive to **Relays** that are
connected to the Announcer. There are only a few Announcers, and these only
accept connections from approved Relays. Most relays connect to multiple
announcers for added redundancy.

The **Relay**, like the Announcer, is a dumb repeater of everything it
receives. Relays receive data from their Announcers, then pipe it out to any
subscribers that are connected to them. Subscribers can be other **Relays**,
or actual user sites/applications.

By using our system of Relays, we keep bandwidth usage and costs
lower on the top-level Announcers. We are also able to keep "fanning out" to
improve redundancy and serve greater numbers of consumers without large
increases in bandwidth utilization.

We are left with a very efficient, very sturdy data relay network. The next
section goes into detail about fault-tolerance.

High Availability through shared burden
---------------------------------------

EMDR is architected in a way that allows every single component to be
replicated. We can easily add additional daemons at each level of the stack in
order to improve availability, or to spread costs.

HTTP Uploads are dispersed to Gateways via Round-Robin DNS, which is a
simple way to distribute the traffic across multiple machines. For each additional
Gateway added to DNS rotation, incoming bandwidth consumption drops for the
whole pool as the load is divided. If at any time one of the gateways becomes
unreachable, it is automatically removed from the DNS rotation.

In the diagram below, we see a rough representation of our current deployment.
Site 1 is comprised of EMDR running on Greg Taylor's (the project maintainer)
machines, and Site 2 is a separate copy running in another data center. The
relays are all ran by different volunteers.

.. note:: We are not limited to just two instances of EMDR, there is no hard
    limit. Additionally, we'll mostly scale by adding more Gateways, since
    additional Announcers are only for redundancy.

At every step of the entire flow, we can afford to lose one of the two
daemons without a service interruption. The infrastructure can be scaled well
out past the initial two sites, if need be.

.. image:: images/emdr-daemon-diagram.png

Security
--------

Security is something we take seriously, but let's consider the current
reality of market data with EVE sites: *Players upload market data directly
to market sites.* We are no less secure than that. Uploads can be faked,
and malicious payloads can be sent, though EMDR will do its best to catch
anything harmful.

.. note:: As a consumer, you may wish to cross-reference incoming data. In
    many cases, you will get the same data point multiple times, as several
    players upload the same thing. This can be used to your advantage.

Technology Used
---------------

This is the least interesting part of the overview, so it goes towards the
ends.

* EMDR is written in Python_.
* All network-related stuff is handled by ZeroMQ_, which is an incredibly
  simple and performant networking library.
* gevent_ is used for their excellent greenlet-based Queue, Workers, and
  async network I/O.
* The gateway HTTP servers run bottle_.

The entire stack is super low overhead, and very fast.

Volunteering
------------

If you would like to volunteer computing resources to the EMDR network,
see :doc:`volunteering` for more details.