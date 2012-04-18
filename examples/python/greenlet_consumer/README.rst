Example EMDR Greenlet Consumer
==============================

This example uses a greenlet pool to accept incoming market data. greenlets
are micro-threads that are extremely lightweight, meaning we can spawn one
for each incoming market message from EMDR.

Before trying this example, make sure to install ZeroMQ, then the requirements::

    pip install -r requirements.txt

You may then run the example::

    python gevent_consumer.py

Suggested next steps
--------------------

Tack on storage to the DB backend of your choice in the worker function.