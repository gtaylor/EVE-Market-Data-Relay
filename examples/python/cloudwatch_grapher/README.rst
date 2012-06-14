Example EMDR Cloudwatch Grapher
===============================

A simple script that listens to EMDR, tracks the number of messages coming in,
and reports it to Amazon CloudWatch_ as a custom metric.

CloudWatch_ allows for nearly real-time graphing from within the AWS Management
Console, and also allows programmatic access to all recorded data. If you
keep the tracking frequency low enough to stay in the free tier (1,000,000
requests per month), this script is free to run.

.. _CloudWatch: http://aws.amazon.com/cloudwatch/

Before trying this example, make sure to install ZeroMQ, then the requirements::

    pip install -r requirements.txt

Then edit the ``AWS_*`` fields within ``cloudwatch_grapher.py`` to add your
AWS API keys.

You may then run the example::

    python cloudwatch_grapher.py

Suggested next steps
--------------------

Customize to chart other metrics that interest you.