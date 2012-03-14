Thundercuddles
==============

:Author: Greg Taylor
:License: BSD

This project is a proof-of-concept for a super-scalable, cheap way to parse
a large amount of market data from EVE Online players, then make said data
available via a basic API.

There are already a number of other great sites that do this well, so we have
to stick to the following principles to make this a worthwhile experiment:

* The application must be able to accept an extremely large number of incoming
  market orders without performance degrading noticeably.
* It must be very easy to scale the system.
* The data must be served in a similar, super-scalable-and-zippy manner.

Current Status
--------------

This project is in early, early development. Unless you are very masochistic,
you probably won't derive any value from it just yet.

Installation
------------

* pip install -r requirements.txt
* ???
* profit

License
-------

This project, and all contributed code, are licensed under the BSD License.
A copy of the BSD License may be found in the repository.
