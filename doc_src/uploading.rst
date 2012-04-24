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

Keep an eye out for HTTP 400 (Invalid input) and 500 (Server errors) while
developing your upload relay. For anything new, we strongly recommend using
the Unified Uploader format, as that is where the bulk of dev time and attention
goes to in EMDR.

**Bonus for Unified Format Uploaders:** EMDR accepts gzipped POST bodies when
using Unified Uploader Interchange Format. zlib/gzip compress your stream and
set your ``Content-Encoding: gzip`` header, and help us both save loads of
bandwidth.

.. warning:: If you choose to re-POST uploads, be careful about also consuming
    the EMDR feed. If your uploader endpoint is saving the uploads, you may
    find yourself in an infinite upload loop. You probably want to look at the
    "Running a Gateway" section.

Running a Gateway
^^^^^^^^^^^^^^^^^

Alternatively, you can post an issue on the `mailing list`_ or
`issue tracker`_ asking about running an HTTP gateway. The gateway would accept
uploads at your site's normal upload location, and would feed to the EMDR
network's Announcers. Your application would then consume the EMDR feed from
EMDR's Announcers.

While there is slightly more bandwidth usage, **this is probably the safest and
easiest of the options**. The EMDR stream is compressed, so even then, the
uptick in bandwidth is pretty small (just the traffic from your Gateway to
2-3 EMDR root Announcers, then consuming from the same Announcer).
