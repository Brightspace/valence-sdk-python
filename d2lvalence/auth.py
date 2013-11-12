# -*- coding: utf-8 -*-
# D2LValence package, auth module.
#
# Copyright (c) 2012 Desire2Learn Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
:module: d2lvalence.auth
:synopsis: Provides auth assistance for Desire2Learn's Valence API client
           applications.
"""

### Authentication ###
# For use with D2LSigner
import base64
import hashlib
import hmac

# For use with D2LAppContext and D2LUserContext
import urllib.parse

# For use with D2LUserContext
import time
from requests.auth import AuthBase


# factory functions
def fashion_app_context(app_id='', app_key=''):
    """Build a new application context using a default D2LSigner.

    :param app_id: D2L-provided Application ID string.
    :param app_key: D2L-provided Application Key string, used for signing.
    """
    s = D2LSigner()
    return D2LAppContext(app_id=app_id, app_key=app_key, signer=s)


def fashion_user_context(app_id='',
                         app_key='',
                         d2l_user_context_props_dict={}):
    """Re-build a user context using a default D2L Signer.

    :param app_id: D2L-provided Application ID string.
    :param app_key: D2L-provided Application Key string, used for signing.
    :param d2l_user_context_props_dict: Context properties dictionary saved
           from a previous user context instance.
    """
    ac = fashion_app_context(app_id=app_id, app_key=app_key)
    return ac.create_user_context(
        d2l_user_context_props_dict=d2l_user_context_props_dict)


# classes
class D2LSigner(object):
    """Default signer class that app and user contexts can use to create
    appropriately signed tokens.
    """

    def get_hash(self, key_string, base_string):
        """Get a digest value suitable for direct inclusion into an URL's
        query parameter as a token.

        Note that Valence API services expect signatures to be generated with
        the following constraints:
        - Encoding keys, and base strings, are UTF-8 encoded
        - HMAC digests are generated using a standard SHA-256 hash
        - Digests are then "URL-safe" base64 encoded (where `-` and `_`
        substitute for `+` and `/`)
        - The resulting string is then stripped of all `=` characters, and all
        leading and trailing whitespace characters

        :param key_string:
            App or User key to use for encoding.

        :param base_string:
            Base string to encode.

        :returns: URL-safe, base64 encoded result of the signing operation
        suitable for adding to a server request.
        """
        k, b = key_string.encode('utf-8'), base_string.encode('utf-8')

        h256 = hmac.new(k, b, hashlib.sha256)
        d = base64.urlsafe_b64encode(h256.digest())
        result = d.decode('utf-8').replace('=', '').strip()

        return result

    def check_hash(self, hash_string, key_string, base_string):
        """Verify that a given digest value was produced by a compatible
        `D2LSigner` given your provided base string and key.
        """
        verify = self.get_hash(key_string, base_string)
        return verify == hash_string


class D2LAuthResult:
    """Enumeration of result situations that `D2LUserContext` instances can
    interpret. """
    UNKNOWN, OKAY, INVALID_SIG, INVALID_TIMESTAMP, NO_PERMISSION = range(5)


class D2LAppContext(object):
    """Generic base class for a Valence Learning Framework API client
    application.
    """

    # route for requesting a user token
    AUTH_API = '/d2l/auth/api/token'

    # Constants for use by inheriting D2LAppContext classes, used to help keep
    # track of of the query parameter names send back by the back-end in the
    # authenticated redirect url
    CALLBACK_URL = 'x_target'
    CALLBACK_USER_ID = 'x_a'
    CALLBACK_USER_KEY = 'x_b'

    # Constants for use by inheriting D2LAppContext classes, used to help keep
    # track of the query parameter names used in Valence API URLs
    SCHEME_U = 'http'
    SCHEME_S = 'https'
    APP_ID = 'x_a'
    APP_SIG = 'x_b'
    TYPE = 'type'

    # the valid user-context connection types understood by the back-end
    VALID_TYPES = ('mobile',)

    def __init__(self, app_id='', app_key='', signer=None):
        """Construct a new authentication app context.

        :param app_id:
            Client application's D2L-provided Application ID string.
        :param app_key:
            Client application's D2L-provided application Key string
            that the application should use for signing.
        :param signer:
            A signer instance that implements D2LSigner.

        :raises ValueError: If you provide `None` for either parameter.
        :raises TypeError: If you don't provide a D2LSigner-derived signer.
        """
        self.signer = None
        self.app_id = self.app_key = ''

        if '' in (app_id, app_key):
            raise ValueError('app_id and app_key must have values.')
        else:
            self.app_id, self.app_key = app_id, app_key

        if not isinstance(signer, D2LSigner):
            raise TypeError('signer must implement D2LSigner')
        else:
            self.signer = signer

    def __repr__(self):
        return repr({'app_id': self.app_id,
                     'app_key': self.app_key,
                     'signer': repr(self.signer)})

    def create_url_for_authentication(self,
                                      host,
                                      client_app_url,
                                      connect_type=None,
                                      encrypt_request=True):
        """Build a URL that the user's browser can employ to complete the user
        authentication process with the back-end LMS.

        :param host:
            Host/port string for the back-end LMS service
            (i.e. `lms.someUni.edu:443`). To this parameter, this method adds
            the appropriate API route and parameters for a user-authentication
            request.
        :param client_app_url:
            Client application URL that the back-end service should redirect
            the user back to after user-authentication.
        :param connect_type:
            Provide a type string value of `mobile` to signal to the back-end
            service that the user-context will connect from a mobile device.
        :param encrypt_request:
            If true (default), generate an URL using a secure scheme (HTTPS);
            otherwise, generate an URL for an unsecure scheme (HTTP).
        """
        sig = self.signer.get_hash(self.app_key, client_app_url)

        # set up the dictionary for the query parms to add
        parms_dict = {self.APP_ID: self.app_id,
                      self.APP_SIG: sig,
                      self.CALLBACK_URL: client_app_url}

        if (connect_type in self.VALID_TYPES):
            parms_dict[self.TYPE] = connect_type

        # the urlunsplit parts needed to build an URL
        scheme = netloc = path = query = fragment = ''
        if encrypt_request:
            scheme = self.SCHEME_S
        else:
            scheme = self.SCHEME_U
        netloc = host
        path = self.AUTH_API
        query = urllib.parse.urlencode(parms_dict, doseq=True)
        result = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

        return result

    def create_anonymous_user_context(self, host, encrypt_requests=False):
        """Build a new anonymous-LMS-user authentication context for a Valence
        Learning Framework API client application.

        :param host:
            Host/port string for the back-end service
            (i.e. `lms.someUni.edu:443`).
        :param encrypt_requests:
            If true, use HTTPS for requests made through the resulting built
            user context; if false (the default), use HTTP.
        """
        if host == '':
            raise ValueError('host must have a value when building a new context.')
        pd = {'host': host,
              'encrypt_requests': encrypt_requests,
              'user_id': '',
              'user_key': '',
              'server_skew': 0}
        r = self.create_user_context(d2l_user_context_props_dict=pd)
        return r

    def create_user_context(self,
                            result_uri='',
                            host='',
                            encrypt_requests=False,
                            d2l_user_context_props_dict={}):
        """Build a new authentication LMS-user context for a Valence Learning
        Framework API client application.

        :param result_uri:
            Entire result URI, including quoted parameters, that the back-end
            service redirected the user to after user-authentication.
        :param host:
            Host/port string for the back-end service
            (i.e. `lms.someUni.edu:443`).
        :param encrypt_requests:
            If true, use HTTPS for requests made through the resulting built
            user context; if false (the default), use HTTP.
        :param d2l_user_context_props_dict:
            If the client application already has access to the properties
            dictionary saved from a previous user context, it can provide it
            with this property. If this paramter is not `None`, this builder
            function ignores the `result_uri` parameter as not
            needed.
        """
        result = None

        # If caller provides existing user context properties, we build with it
        if d2l_user_context_props_dict:
            t = d2l_user_context_props_dict
            result = D2LUserContext(host=t['host'],
                                    user_id=t['user_id'],
                                    user_key=t['user_key'],
                                    app_id=self.app_id,
                                    app_key=self.app_key,
                                    encrypt_requests=t['encrypt_requests'],
                                    server_skew=t['server_skew'],
                                    signer=self.signer)
        # If the caller did not provide an existing user context properties
        # dict, we use the other parms to create a new user context
        else:
            if '' in (result_uri, host):
                raise ValueError('result_uri and host must have values when building new contexts.')

            parts = urllib.parse.urlsplit(result_uri)
            scheme, netloc, path, query, fragment = parts[:5]
            parsed_query = urllib.parse.parse_qs(query)
            uID = parsed_query[self.CALLBACK_USER_ID][0]
            uKey = parsed_query[self.CALLBACK_USER_KEY][0]
            if uID and uKey:
                result = D2LUserContext(host=host,
                                        user_id=uID,
                                        user_key=uKey,
                                        app_id=self.app_id,
                                        app_key=self.app_key,
                                        encrypt_requests=encrypt_requests,
                                        signer=self.signer)

        return result


##
## Inherits from AuthBase so that we can use a user context as an AuthBase
## helper calls made through the Requests package.
##
class D2LUserContext(AuthBase):
    """Calling user context that a Valence Learning Framework API client
    application will use for all API calls.  """

    # Constants for use by inheriting D2LUserContext classes, used to help keep
    # track of the query parameter names used in Valence API URLs.
    SCHEME_P = 'http'
    SCHEME_S = 'https'

    APP_ID = 'x_a'
    APP_SIG = 'x_c'
    USER_ID = 'x_b'
    USER_SIG = 'x_d'
    TIME = 'x_t'

    def __init__(self, host='', user_id='', user_key='', app_id='', app_key='',
                 encrypt_requests=False, server_skew=0, signer=None):
        """Constructs a new authenticated calling user context.

        Clients are not intended to invoke this constructor directly; rather
        they should use the `D2LAppContext.create_user_context()` factory
        method, or the `fashion_user_context()` factory function.

        :param hostName: Host/port string for the back-end service.
        :param user_id: User ID provided by the back-end service to the
                        authenticated client application.
        :param user_key: User Key provided by the back-end service to the
                         authenticated client application.
        :param encrypt_requests: If true, use HTTPS for requests made through
                                 this user context; if false (the default), use
                                 HTTP.
        :param server_skew: Time skew between the service's time and the client
                            application's time, in milliseconds.
        :param signer: A signer instance that implements D2LSigner.

        :raises TypeError: If you provide a signer that doesn't implement
                           `D2LSigner`.
        :raises ValueError: If you provide `None` for hostName, port, user_id,
                            or user_key parameters.
        """
        self.signer = None
        self.scheme = self.SCHEME_P
        if encrypt_requests:
            self.scheme = self.SCHEME_S
        self.host = self.user_id = self.user_key = self.app_id = self.app_key = ''

        if (user_id == '') != (user_key == ''):
            raise ValueError('Anonymous context must have user_id and user_key empty; or, user context must have both user_id and user_key with values.')
        elif '' in (host, app_id, app_key):
            raise ValueError('host, app_id, and app_key must have values.')
        else:
            self.host = host
            self.user_id = user_id
            self.user_key = user_key
            self.app_id = app_id
            self.app_key = app_key
            self.encrypt_requests = encrypt_requests
            self.server_skew = server_skew

        if self.user_id == '':
            self.anonymous = True
        else:
            self.anonymous = False

        if not isinstance(signer, D2LSigner):
            raise TypeError('signer must implement D2LSigner')
        else:
            self.signer = signer

    # Entrypoint for use by requests.auth.AuthBase callers
    def __call__(self, r):
        # modify requests.Request `r` to patch in appropriate auth goo

        method = scheme = netloc = path = query = fragment = ''

        parts = urllib.parse.urlsplit(r.url)
        scheme, netloc, path, query, fragment = parts[:5]

        qparms_dict = urllib.parse.parse_qs(query)

        method = r.method.upper()
        time = self._get_time_string()
        # return path to its original, un-URL quoted state
        bs_path = urllib.parse.unquote_plus(path.lower())
        base = '{0}&{1}&{2}'.format(method, bs_path, time)

        app_sig = self.signer.get_hash(self.app_key, base)
        if self.anonymous:
            usr_sig = ''
        else:
            usr_sig = self.signer.get_hash(self.user_key, base)

        # set up the dictionary for the query parms to add
        parms_dict = {self.APP_ID: [self.app_id],
                      self.APP_SIG: [app_sig],
                      self.USER_ID: [self.user_id],
                      self.USER_SIG: [usr_sig],
                      self.TIME: [time]}
        qparms_dict.update(parms_dict)
        query = urllib.parse.urlencode(qparms_dict, doseq=True)

        r.url = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

        return r

    def __repr__(self):
        result = self.get_context_properties()
        result.update({'signer': repr(self.signer)})
        return repr(result)

    def _get_time_string(self):
        # we must pass back seconds; time.time() returns seconds, server_skew is in millis
        t = int(round(time.time() + (self.server_skew/1000)))
        return str(t)

    def create_authenticated_url(self,
                                 api_route='/d2l/api/versions/',
                                 method='GET'):
        """Create a properly tokenized URL for a new request through this user
        context.

        :param api_route: API to invoke on the back-end service (get all
        versions route by default).
        :param method: Method for the request (GET by default, POST, etc).

        :returns: URI string you can fashion into an HTTP request, containing
        the time-limited authentication token parameters needed for a Valence
        API call.
        """
        time = self._get_time_string()
        # return path to its original, un-URL quoted state
        bs_path = urllib.parse.unquote_plus(api_route.lower())
        base = '{0}&{1}&{2}'.format(method.upper(), bs_path, time)

        app_sig = self.signer.get_hash(self.app_key, base)
        if self.anonymous:
            usr_sig = ''
        else:
            usr_sig = self.signer.get_hash(self.user_key, base)

        parms_dict = {self.APP_ID: self.app_id,
                      self.APP_SIG: app_sig,
                      self.USER_ID: self.user_id,
                      self.USER_SIG: usr_sig,
                      self.TIME: time}

        # the urlunsplit parts needed to build an URL
        scheme = netloc = path = query = fragment = ''
        if self.encrypt_requests:
            scheme = self.SCHEME_S
        else:
            scheme = self.SCHEME_P
        netloc = self.host
        path = api_route
        query = urllib.parse.urlencode(parms_dict)
        result = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

        return result

    # Currently, this function does very little, and is present mostly for
    # symmetry with the other Valence client library packages.
    def interpret_result(self, result_code, response, logfile=None):
        """Interpret the result made for an API call through this user context.

        :param result_code:
            The HTTP result code from the response; if a successful result
            (2xx), this method ignores the response.
        :param response:
            Response passed back by the back-end service. The precise form of
            this is implementation dependent. It could be a string, or a file
            object, or a Response object of some kind.
        :param logfile:
            Optional. A caller might want to provide a file stream for logging
            purposes; if present, this method should write logging messages to
            this file stream.

        :returns: One of the enumerated D2LAuthResult class variables.
        """
        result = D2LAuthResult.UNKNOWN

        if result_code == 200:
            result = D2LAuthResult.OKAY
        elif result_code == 401:
            result = D2LAuthResult.INVALID_SIG
        elif result_code == 403:
            # Might also be timestamp issues here?
            result = D2LAuthResult.NO_PERMISSION

        return result

    def get_context_properties(self):
        """Retrieve a dictionary of this calling user context's current state,
        suitable for rebuilding this user context at a later time.
        """
        cp = {'host': self.host,
              'user_id': self.user_id,
              'user_key': self.user_key,
              'encrypt_requests': self.encrypt_requests,
              'server_skew': self.server_skew,
              'anonymous': self.anonymous}
        return cp

    def set_new_skew(self, new_skew):
        """Adjust the known time skew between the local client using this
        user context, and the back-end service.

        :param newSkewMillis: New server time-skew value, in milliseconds.
        """
        self.server_skew = new_skew
