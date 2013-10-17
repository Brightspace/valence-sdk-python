======================================
Desire2Learn Client Library for Python
======================================

This :py:mod:`d2lvalence.auth` module provides assistance for the authentication
needed to invoke Valence APIs. You use the module's functions (and perhaps also
classes) to create a :py:class:`calling user context
<d2lvalence.auth.D2LUserContext>` object that you can then employ in conjunction
with the Reqeusts package as an authentication helper.

You can find the 
`latest build <http://code.google.com/p/desire2learn-valence/downloads/list?q=label:pythonlatestclient>`_
of the client library SDK on our repository download page.

**Dependencies**. In order to use the Python client library SDK, you'll need to
first ensure you have a working Python development environment:

* Python 3 (the reference environment uses Python 3.3).

* The `Requests Python package <http://docs.python-requests.org/en/latest/index.html>`_
  gets used in our :py:mod:`auth <d2lvalence.auth>` module so that you can use a
  calling user context object as an authentication helper for Requests.

* The `Bottle Python package <http://bottlepy.org/docs/dev/>`_ if you want to
  use the samples available in conjunction with this client library (not a
  dependency for the client library itself).


Where'd d2lvalence.data and d2lvalence.service go?
==================================================
The data and service modules have been decoupled from this package going
forward. Continued support for them may appear in a separate `d2lvalence-util`
package.
