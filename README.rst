======================================
Desire2Learn Client Library for Python
======================================
The Python library divides functionality into a number of modules. The primary
module helps with authentication. Several supporting modules can assist with
making calls in several areas of the Valence API.

**Authentication**. The :py:mod:`d2lvalence.auth` module provides assistance for
the authentication needed to invoke Valence APIs. You use the module's functions
(and perhaps also classes) to create a 
:py:class:`calling user context <d2lvalence.auth.D2LUserContext>` object that
you can then employ in conjunction with the Requests package as an
authentication helper.


Installation
============
You can find the source for our Python client library SDK in two locations:

* Our own `Python client GitHub repository <https://github.com/Desire2Learn-Valence/valence-sdk-python>`_. 

* On the PyPi `package index repository <http://pypi.python.org/pypi/D2LValence>`_,
  so you can install it as a package with pip or easy_install.

**Dependencies**. In order to use the Python client library SDK, you'll need to
first ensure you have a working Python development environment:

* Python 3 (the reference environment uses Python 3.5), or Python 2.7 (via the
  use of the future library).

* The `Requests Python package <http://docs.python-requests.org/en/latest/index.html>`_
  gets included in our :py:mod:`auth <d2lvalence.auth>` module so that you can use a
  calling user context object as an authentication helper for Requests.

* The `python-future <http://python-future.org/index.html>`_ library gets used
  to provide Python 2.7 compatibility.

* The `Bottle Python package <http://bottlepy.org/docs/dev/>`_ if you want to
  use the samples available in conjunction with this client library (not a
  dependency for the client library itself).
