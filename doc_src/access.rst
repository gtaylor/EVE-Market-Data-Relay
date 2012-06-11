.. _access:

.. include:: global.txt

Getting access to the EMDR network
==================================

In order to get access to the EMDR network, you will merely need to connect
to a relay. For your convenience, we have listed the relays below that have
available capacity.

==========================================  ==================  ==============  ==================  ====================================================================
URI                                         ISP                 Location        Access              Notes
==========================================  ==================  ==============  ==================  ====================================================================
tcp://relay-us-central-1.eve-emdr.com:8050  Ubuquity Hosting    Chicago, IL     Open                Use this relay if you have no preference.
tcp://emdr-relay.eve-aim.com:8050           Linode              Newark, NJ      Open - See Notes    This is only available to other Linodes in the Newark, NJ location.
==========================================  ==================  ==============  ==================  ====================================================================

Once you have chosen a relay, simply adapt the sample in
:doc:`using` to use the hostname/port of the relay of your choice.

.. note:: Some relays, marked as *Restricted*, require that you request
    access to use them. You will need to get in touch with the relay via the
    contact info listed to work it out with the admin.