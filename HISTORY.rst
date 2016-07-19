.. :changelog:

History
-------

1.2.2 (2016-07-19)
++++++++++++++++++
* Update UserContext.decorate_url_with_authentication() to be a bit more canny
  about the input it gets: if it gets an APIURL with no scheme or netloc, then
  it will attempt to provide those values, taking them from the user context's
  internal state (it already knows the scheme and host it should use for
  decorating routes, to it assumes that it should use those for APIURLs that
  don't have them -- this is a reasonable, but also potentially fragile,
  assumption).
  

1.2.1 (2016-02-25)
++++++++++++++++++
* Roll to 1.2.1 to cope with PyPi not allowing re-use of a release filename
  that's been deleted.


1.2.0 (2016-02-25)
++++++++++++++++++
* Update package to use the `python-future <http://python-future.org/index.html>`
  library to add Python 2 compatibility.


1.1.1 (2014-05-26)
++++++++++++++++++
* Added some validation around user context method accepting API routes to
  tokenize, to catch passing invalid characters for URL paths.

* Updated package requirements to signal support for Python 3.4.


1.1.0 (2013-11-18)
++++++++++++++++++
* Added `D2LUserContext.decorate_url_with_authentication()` to accept an entire URL
  and generate Valence authentication tokens for it; re-factor D2LUserContext
  to pull out the token generation code into an internal method
  (`_build_tokens_for_path()`).


1.0.1 (2013-11-12)
++++++++++++++++++
* PEP8-ified the code; left some long lines for clarity, though.

* Cleaned up README contents.


1.0.0 (2013-10-01)
++++++++++++++++++
* Split away d2lvalence.data and d2lvalence.service from the auth
  library. Further support for these two modules may appear in a future
  `d2lvalence-util` package.

* Re-casting of internally used HTTP scheme constants to be lower-case strings
  to provide wider support for various versions of the `requests` library.


0.1.15 (2013-05-22)
+++++++++++++++++++
* added structures and routes for support user activation

* repair news item attachment upload (in create_news_item_for_orgunit) to avoid
  tacking on extra CR-LF pairs to file data

* broad change to the way dictionaries of control values get passed down from
  the `service` into the requests library, for two reasons: to attempt to
  simplify the code around setting them, and to attempt to better avoid stomping
  values passed down from higher calling layers

* provide a `data.D2LDebugInfo` to act as a carrier for the actual
  request/response object used in the bowels of a service function call: passing
  down a `D2LDebugInfo` in a `d2ldebug` keyword argument captures a ref of the
  request/response used so that you can inspect it after making the service call
  (for examining outgoing URL/headers, full response headers/body/reason, etc)

* factor `Response.raise_for_status()` call into the `_fetch_content()` private
  service method to put it in one place, and to allow us the opportunity to
  gather the response object into a provided `D2LDebugInfo` before possibly
  raising the exception for a failed call

* added `with_traceback()` to the various exceptions service libarary raises for
  more provided trace info on exceptions

* added more type checking around parameters passed into service functions that
  are expected to be D2LValence data classes

* repaired post to create a discussion post to account for being able to send
  one or more file attachments along with the new post; added
  `data.D2LDiscussionPostAttachment` child of `data.D2LFile` to handle
  discussion post attachments

* repaired `service.check_versions()` to consume an array of
  SupportedVersionRequest objects

* fixed bug in `data.CreateCourseOffering.fashion_CreateCourseOffering` factory
  function to set `Path` property for the new instance

* added service function to retrieve a raw news item attachment for a news item
  in an org unit

* added structures and routes to support ePortfolio package export and import

0.1.14 (2013-04-29)
+++++++++++++++++++
* repaired D2LUserContext so that it (a) handles API routes that contain
  characters that would URL-escaped in both it's AuthBase implementation *and*
  its :func:`create_authenticated_url` method, and (b) does this handling in the
  same way that does D2L authentication on other language platforms.

0.1.13 (2013-04-17)
+++++++++++++++++++
* enhanced `service` functions to allow for passing keyword args down into the
  requests library making the outgoing HTTP calls

* explicitly added 'application/json' content type header to service actions
  sending JSON to the service

* modified multipart/mixed upload functions in `service` module to cope with
  changes in requests v1.2.0 around setting the Content-Type header for the
  upload action: now the functions use sessions around a prepped-request object,
  consistent with requests library new pattern for messing with the headers/body
  of an HTTP request

* added `data.D2LNewsAttachment` child of `data.D2LFile` to handle adding
  attachments to news events; added `data.NewsItemData` structure to support
  creation of news events; added new routes to support more news actions

* added `data.CreateEnrollmentData` structure to handle structure sent during
  enrollment creation; added service routes around user enrollment (delete,
  create)

* added `data.GroupCategoryDataFetch` and service methods to support some group
  routes; added routes around group org units

* added `data.GradeObjectCreateData` and re-factored `data.GradeObject`, as well
  as the derived grade object type classes, to separate structures for fetching
  and creating grade objects; added `data.GradeObjectCategory` and
  `data.GradeObjectCategoryData` to support grade object category routes; added
  service routes around grade objects, grade categories, grade values


* added factory methods to the incoming-grade-value structures for easier
  creation; added `data.IncomingFinalAdjustedGradeValue` structure for updating
  final adjusted grade value

* added data structures and routes around course completion

* added routes around calendar events

* fixed `service.get_organization_info` to return an Organization JSON
  structure, and not raw request content.

* fixed `service.get_all_my_grade_values_for_org` to return grade value
  instances, instead of grade object instances

0.1.12 (2013-01-23)
+++++++++++++++++++
* fixed bug in D2LUserContext's implementation as a requests.auth.AuthBase so
  that it more properly handles API routes that contain characters that would be
  URL escaped by the requests library

0.1.11 (2013-01-04)
+++++++++++++++++++
* revised `auth.D2LAppContext.create_url_for_authentication` to include an
  `encrypt_request` parameter (true by default) to allow generation of
  for-authentication URLs that do not use HTTPS

* added `data.D2LDropboxSubsmission` and several service functions to fill out
  support for the dropbox routes

* fixed parm name in get dropbox folder route

* fixed the `ExternalEmail` properties for `data.CreateUserData` and
  `data.UpdateUserData` to provide better support for having `None` values
  (which will translate to `null` when serialized to JSON)

* added `service.update_user()` for updating user records

* fixed the `RoleId` property for `data.CreateUserData` to have an empty default
  value rather than a numeric default (which probably isn't a useful default for
  anyone)

* added `data.UserPasswordData` and service methods to support the user password
  routes (deleting, changing, resetting)

* added `data.Organization` and `data.OrgUnit` and service methods to support
  routes that query the org structure

* added `data.EnrollmentData` and service functions to fill out support for
  enrollment routes

* added `data.IncomingGradeValue` and its derived classes, and service functions
  to fill out support for grades routes

* added `data.NewsItem` and several service functions to fill out support for
  the news routes

* added support to `service` module to try and support pre-1.0.0 requests
  package as well as post-1.0.0 versions.

0.1.10 (2012-12-18)
+++++++++++++++++++
* revised `data` and `service` modules to update for compatibility with requests
  package post version 1.0.0

0.1.9 (2012-10-15)
++++++++++++++++++
* added data and service functions for Learning Repostory routes

* added data and service functions for course offering and content routes

* added data and service functions for discussion forum routes
* renamed utility functions in `data` module used for property set/getting to
  suggest they should be internal and not directly used

* added default (empty) value for `DescriptorDict` property to the
  `data.D2LLockerFile` class

* added `files` named parameter to post and put utility methods for simple file
  post/puts

* fix `service.rename_group_locker_folder()` to properly form route

* cleanup service module to python-ify parameter names

0.1.8 (2012-08-30)
++++++++++++++++++
* added support to the `auth` module for building an anonymous user context
  (context with no user ID/Key pair) -- clients can use such a context to make
  calls to the various API Property/Version routes to query LMS for API versions

* moved auth to use direct `==` comparison to check for empty parameters instead
  of use `in (singleItemList,)` pattern

* factored out process of fetching contents of Requests objects into a single
  funtion, moved to examine `request.headers['content.type']` to determine how
  to handle contents rather than just `try` to fetch r.JSON and default to
  r.content

* repaired `service.check_versions()` to pass the `supported_version_request_array`
  as json data

* fixed `service._simple_upload()` to seek underlying buffer stream to head
  position before and after read, instead of trying to seek on the byte-string
  we read the stream into

* added support to the `service` library for distinguishing between anonymous and
  non-anonymous user contexts, and let version calls be made with anonymous
  contexts, raise errors in the case of all other calls that demand a user context

* added more grade routes for fetching 'my' grades

0.1.7 (2012-08-10)
++++++++++++++++++
* added `service.get_profile_by_user_id()`

* added `data.LockerItem`, `data.LockerFolder`, `data.GroupLocker` to support
  locker operations

* added to suite of locker functions to the `service` module to assist with locker
  operations: this includes an example of how you might want to handle the
  "simple upload" process for those Valence routes that use simple file upload

0.1.6 (2012-07-13)
++++++++++++++++++
* Fix bug in `update_social_media_url_by_url()`... we should look
  for 'url'-keyed entries, not 'name'-keyed entries

* Some documentation revisions

* Remove 'exceptions' module as not utilized

0.1.5 (2012-07-11)
++++++++++++++++++
* Changed `D2LStructure.as_json()` to kick back a deep-copy of the encapsulated
  data, instead of a ref to the instance's internal data structure

* Bug fixes

0.1.4 (2012-07-06)
++++++++++++++++++
* Refactoring and re-building of the libraries: moved data-structures into
  `data` module and service-related functions into `service` module;
  auth-related functionality remains in `auth`

* Re-worked samples to be more in line with design for the other client
  libraries

0.1.0 (2012-06-02)
++++++++++++++++++
* Initial version

