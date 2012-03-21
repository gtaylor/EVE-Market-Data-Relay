EVE Market Data Relay
=====================

:Author: Greg Taylor
:License: BSD

This project is a proof-of-concept for a super-scalable, affordable way to
accept a large amount of user-submitted market data (via uploaders), and
re-broadcast said data in realtime to a number of subscribers.

The end result is that those writing market-data driven applications could
simply subscribe to a "firehose" of market data, and get going, without having
to hassle with uploaders or data submission APIs.

Project Motivation
------------------

The reason for this project's existence is that there are currently a large
number of barriers to entry for people wishing to start a project that relies
on EVE market data. A developer would probably need to:

* Either write their own uploader client, or re-purpose an existing uploader.
* Write a service/API to accept the data in whatever format(s) the uploader(s)
  they'd like to support use.
* Actually get players to point their uploader at said service/API (This is the
  hardest part!)
* Then, and only then, start writing the *fun* part of their application as
  the amount of data coming in slowly grows. By this point, they are probably
  a way down the road to burnout.

If we can get some sort of a following organized around an instance of this
application, anyone wishing to work on a market-data driven project could
simply subscribe to our firehose of EVE market data.

Core Principles
---------------

* The application must be able to accept an extremely large number of incoming
  market orders without performance degrading noticeably.
* It must be very easy to scale the system.
* The broadcasting of the market data needs to happen in a "fan out" manner.
  In this way, we can keep adding additional subscribers without running into
  scalability issues.

How it all fits together
------------------------

For any given submitted market order, here is the flow said order goes through::

    (Gateway) -> (Processor) -> (Relay)

First, the order hits the **Gateway**, which is a very light WSGI application.
The only purpose of the gateway is to queue the order for submission to one of
many **Processor** daemons. The number of processor daemons can scale up and
down without any modifications or restarts of the **Gateway**.

The message gets passed from the **Gateway** to the **Processor** via
ZeroMQ_, which is an extremely scalable and performant transport/messaging
layer. The **Processor** looks at the raw data, parses it, performs some
really simple validation/verification, then passes it on to our top level
**Relay** via ZeroMQ_.

The **Relay** is a dumb repeater daemon. It takes the processed orders and just
spews them out to any subscribers. Subscribers can be other **Relay** daemons,
or actual user sites/applications. In the case of our eventual production
deployment, the top-level (tier-1) **Relay** will only speak to other relays.
The second level (tier-2) relays and lower are the ones that other
sites/applications can actually use. This keeps the load on our
top-level (tier-1) relay to a minimum, *meanwhile, allowing anyone to volunteer
to run tier-2 relays*.

.. _ZeroMQ: http://www.zeromq.org/

Current Status
--------------

This project is in early, early development. This is all very experimental,
so documentation is likely to be minimal until things start settling.

Installation
------------

* pip install -r requirements.txt
* ???
* profit

License
-------

This project, and all contributed code, are licensed under the BSD License.
A copy of the BSD License may be found in the repository.
