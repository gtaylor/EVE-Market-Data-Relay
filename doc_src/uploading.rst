.. _uploading:

.. include:: global.txt

Uploading Market data to EMDR
=============================

Uploading to EMDR contributes data to for public use. Feeding the firehose
benefits us all, so please do consider pointing your uploader at the network.

With the EVE Marketeer Client
-----------------------------

For those gracious souls willing to point their uploaders at EMDR, here how you
can do that.

* Download/install the `EVE Marketeer Uploader`_.
* Run the application.
* Go to the Endpoints tab.
* Hit 'Add'.
* Enter 'EMDR' for the name.
* Leave data type as EVE Marketeer & Marketdata.
* Set the URL to: http://master.eve-emdr.com/upload/eve_marketeer/
* Enter 46 for upload key.
* Hit Save.
* You're all set. Get uploading!

You can then use any market service's auto-uploader pages.

.. _EVE Marketeer Uploader: http://www.evemarketeer.com/uploader

Uploaders with Unified Uploader Support
---------------------------------------

If your uploader is listed below, it supports Unified Upload Format, and can
upload in a more direct manner (for us):

* Contribtastic for Mac

Use the following URL for uploading:

* http://master.eve-emdr.com/upload/unified/

We'll expand the list of uploaders as more support this format.

Syndicating your Market Site's upload data to EMDR
--------------------------------------------------

For those with your own market site who wish to share data, there are a few
relatively easy ways to do so. While we recognize that this represents
additional work on your part, the greater EVE community benefits from the
combination of market data.

If you run into issues syndicating your data, post on the `mailing list`_
or `issue tracker`_ and we'll do everything we can to help.

Re-posting incoming data to EMDR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each incoming upload, re-POST it to EMDR's uploader endpoints. There are
different end points for different market data formats:

* EVE Marketeer and EVE Marketdata format: http://master.eve-emdr.com/upload/eve_marketeer/
* Unified Uploader Interchange Format: http://master.eve-emdr.com/upload/unified/

Almost all traffic will probably be the former, at this point. You'd need
to simply preserve the POST keys and send them our way.

.. warning:: If you go this route, be careful about also consuming the EMDR
    feed. If your uploader endpoint is saving the uploads, you'll get duplicate
    data from EMDR, since you fed it with said data.

Running a Gateway
^^^^^^^^^^^^^^^^^

Alternatively, you can post an issue on the `mailing list`_ or
`issue tracker`_ asking about running an HTTP gateway. The gateway would accept
uploads at your site's normal upload location, and would feed directly to EMDR.
Your application would then consume the EMDR feed.

This is probably the safest and easiest of the options.