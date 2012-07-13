.. _uploading:

.. include:: global.txt

Uploading Market data to EMDR
=============================

Uploading to EMDR contributes data to for public use. Feeding the firehose
benefits us all, so please do consider pointing your uploader at the network.

With EVEMon
-----------

To upload data with EVEMon_, you need only have it installed and running.
Market data is uploaded to EMDR by default.

.. _EVEMon: http://evemon.battleclinic.com/

With EMDU (Mac, Linux, and Windows)
-----------------------------------

EMDU_ (EVE Market Data Uploader) is a cross-platform, console-based market
uploader client. It uploads directly to EMDR. For those who are running
Mac or Linux, this client should run beautifully for you. It runs on Windows,
as well, but it's probably easier to install EVEMon.

See the the `install instructions`_ for how to get started.

.. _install instructions: https://github.com/gtaylor/EVE-Market-Data-Uploader/blob/master/README.rst

With other clients
------------------

While we prefer EVEMon, you can use any client that supports the
`Unified Uploader Data Interchange Format`_. An up to date list is maintained
here: `Clients supporting UUDIF`_.

Steps vary from client to client, but here is the typical process:

* Open the dialog that lets you specify where to send market data.
* Create a new endpoint. Select Unified format if it asks.
* Set the URL to: http://upload.eve-emdr.com/upload/
* Enter your upload key, if you feel like it. Otherwise, just make something
  up or leave it blank.
* Hit save, and start uploading.

You can then use any market service's auto-uploader pages.
