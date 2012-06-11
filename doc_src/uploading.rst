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

With the EVE Marketeer Client
-----------------------------

While we prefer EVEMon, you can use the EVE Marketeer Client as well:

* Download/install the `EVE Marketeer Uploader`_.
* Run the application.
* Go to the Endpoints tab.
* Hit 'Add'.
* Enter 'EMDR' for the name.
* Leave data type as EVE Marketeer & Marketdata.
* Set the URL to: http://upload.eve-emdr.com/upload/
* Enter EMDR for upload key.
* Hit Save.
* You're all set. Get uploading!

You can then use any market service's auto-uploader pages.

.. _EVE Marketeer Uploader: http://www.evemarketeer.com/uploader

Other Clients
-------------

Any client that supports either Unified Uploader Interchange format, or
EVE Marketeer/EVE Market Data format will also work just fine. The following
clients fall under this designation:

* Contribtastic for Mac

Simply point your client at: http://upload.eve-emdr.com/upload/

The message format will be auto-detected and parsed accordingly.
