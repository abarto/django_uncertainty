django\_uncertainty
===================

Introduction
------------

``django_uncertainty`` is a `Django <https://www.djangoproject.com/>`_ middleware that allows the
developer to introduce controlled uncertainty into his or her site. The main purpose is providing a
tool to reproduce less-than-ideal conditions in a local development environment to evaluate
external actors might react when a Django site starts misbehaving.

It requires `Django 1.10 <https://docs.djangoproject.com/en/1.10/releases/1.10/>`_ or later as it
uses the new middleware framework.

Installation
------------

You can get ``django_uncertainty`` using pip:

$ pip install django\_uncertainty

If you want to install it from source, grab the git repository from
GitHub and run setup.py:

::

    $ git clone git://github.com/abarto/django_uncertainty.git
    $ cd django_uncertainty
    $ python setup.py install

Once the package has been installed, you need to add the middleware to
your Django settings file:

::

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        ...
        'uncertainty.UncertaintyMiddleware'
    ]

Usage
-----

The middleware behaviour is controlled by the ``DJANGO_UNCERTAINTY`` Django setting. For example:

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(
        u.path_matches('^/api'), u.random_choice([
            (u.delay(u.default(), 5), 0.3), (u.server_error(), 0.2)]))

This tells the middleware that if the request path starts with "/api", 30% of the time the request
is going to be delayed by 5 seconds, 20% of the time the site is going to respond with a status 500
(Server Error), and the rest of the time the site is going to function normally.

The next section describes all the available behaviours and conditions.

Behaviours
----------

All behaviours are implemented as sub-classes of the ``Behaviour``
class:

::

    class Behaviour:
        """Base of all behaviours. It is also the default implementation which just just returns the
        result of calling get_response."""
        def __call__(self, get_response, request):
            """Returns the result of calling get_response (as given by the UncertaintyMiddleware
            middleware with request as argument. It returns the same response that would have been
            created by the Django stack without the introduction of UncertaintyMiddleware.
            :param get_response: The get_response method provided by the Django stack
            :param request: The request that triggered the middleware
            :return: The result of calling get_response with the request parameter
            """
            response = get_response(request)
            return response

Behaviours work like functions that take the same parameters given the
the Django middleware.

default
~~~~~~~

As the name implies, this is the default behaviour. It just makes the requests continue as usual
through the Django stack. Using ``default`` is the same as omitting the ``DJANGO_UNCERTAINTY``
setting altogether.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.default()

html
~~~~

Overrides the site's response with an arbitrary HTTP response. Without any arguments it returns a
response with status code 200 (Ok). ``html`` takes the same arguments as Django's
`HttpResponse <https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpResponse>`_.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.html('<html><head></head><body><h1>Hello World!</h1></body></html>')

ok
~~

An alias for ``html``.

bad\_request
~~~~~~~~~~~~

Overrides the site's response with an HTTP response with status code 400 (Bad Request).
``bad_request`` takes the same arguments as Django's
`HttpResponseBadRequest <https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpResponseBadRequest>`_.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.bad_request('<html><head></head><body>Oops!</body></html>')

forbidden
~~~~~~~~~

Overrides the site's response with an HTTP response with status code 403 (Forbidden). ``forbidden``
takes the same arguments as Django's
`HttpResponseForbidden <https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpResponseForbidden>`_.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.forbidden('<html><head></head><body>NOPE</body></html>')

not\_allowed
~~~~~~~~~~~~

Overrides the site's response with an HTTP response with status code 405 (Not Allowed).
``not_allowed`` takes the same arguments as Django's
`HttpResponseNotAllowed <https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpResponseNotAllowed>`_.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.not_allowed(permitted_methods=['PUT'], content='<html><head></head><body>NOPE</body></html>')

not\_found
~~~~~~~~~~

Overrides the site's response with an HTTP response with status code 404 (Not Found).
``not_found`` takes the same arguments as Django's
`HttpResponse <https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpResponse>`_.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.not_found(permitted_methods=['PUT'], content='<html><head></head><body>Who?</body></html>')

server\_error
~~~~~~~~~~~~~

Overrides the site's response with an HTTP response with status code 500 (Internal Server Error).
``server_error`` takes the same arguments as Django's
`HttpResponseServerError <https://docs.djangoproject.com/en/1.10/ref/request-response/#django.http.HttpResponseServerError>`_.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.server_error('<html><head></head><body>BOOM</body></html>')

status
~~~~~~

Overrides the site's response with an HTTP response with a given status code.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.status(201, content='<html><head></head><body><h1>Created</h1></body></html>')

json
~~~~

Overrides the site's response with an arbitrary HTTP response with content type
``application/json``. Without any arguments it returns a response with status code 200 (Ok).
``json`` takes the same arguments as Django's
`JsonResponse <https://docs.djangoproject.com/en/1.10/ref/request-response/#jsonresponse-objects>`_.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.json({'foo': 1, 'bar': True})

delay
~~~~~

Introduces a delay after invoking another behaviour. For example, this specifies a delay of half a
second into the actual site responses:

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.delay(u.default(), 0.5)

You can replace the first argument with any other valid behaviour.

delay\_request
~~~~~~~~~~~~~~

It is similar to ``delay``, but the delay is introduced *before* the specified behaviour is invoked.

random\_choice
~~~~~~~~~~~~~~

This is the work horse of ``django_uncertainty``. ``random_choice`` allows you to specify different
behaviours that are going to be chosen at random (following the give proportions) when a request is
received. It takes a list of behaviours or tuples of behaviours and proportions,

For example, let's say we want 30% of the request to be responded with an Internal Server Error
response, 20% with a Bad Request response, and the rest with the actual response but with a 1
second delay. This can be specified as follows:

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.random_choice([(u.server_error(), 0.3), (u.bad_request(), 0.2), u.delay(u.default(), 1)])

If proportions are specified, the total sum of them must be less than 1. If no proportions are
specified, the behaviours are chosen with an even chance between them:

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.random_choice([u.server_error(), u.default()])

This specifies that approximetly half the request are going to be responded with an Internal Server
Error, and half will work normally.

conditional
~~~~~~~~~~~

It allows you to specify that a certain behaviour should be invoked only if a certain condition is
met. If the condition is not met, the alternative behvaiour (which is ``default`` by default) is
executed.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.conditional(u.is_post, u.server_error())

The specification above states that if the request uses the POST method, the site should respond
with an Internal Server Error. If you want to specify an alternative behaviour other than the
default, use the ``alternative_behaviour`` argument:

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.conditional(u.is_post, u.server_error(), alternative_behaviour=u.delay(u.default(), 0.3)

Conditions can be combined using boolean operators. For instance,

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.conditional(u.is_authenticated | -u.is_get, u.bad_request())

specifies that if the request is authenticated or if it uses the GET method, a Bad Request response
should be used.

In the next section, all the predefined conditions are presented.

cond
~~~~

An alias for ``conditional``.

multi\_conditional
~~~~~~~~~~~~~~~~~~

``multi_conditional`` takes a list of condition/behaviour pairs, and when a request is received, it
iterates over the conditions until one is met, and the corresponding behaviour is invoked. If no
condition is met, the default behaviour is invoked.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.multi_conditional([(u.is_get, u.delay(u.default(), 0.5), (u.is_post, u.server_error())])

The specification above states that if the request uses the GET method, it should be delayed by
half a second, if it uses POST, it should respond with an Internal Server Error, and if neither of
those conditions are met, the request should go through as usual.

The default behaviour to be used when no conditions are met can be specified with the ``default_behaviour`` argument:

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.multi_conditional(
        [
            (u.is_get, u.delay(u.default(), 0.5),
            (u.is_post, u.server_error())
        ], default_behaviour=u.not_found())

multi\_cond
~~~~~~~~~~~

An alias for ``multi_conditional``.

case
~~~~

An alias for ``multi_conditional``.

Custom behaviours
~~~~~~~~~~~~~~~~~

We've done our best to implement behaviours that make sense in the context of introducing
uncertainty into a Django site, however, if you need to implement your own behaviours, all you need
to do is derive the ``Behaviour`` class. Let's say you want a Behaviour that adds a header to the
response generated by another behaviour. Here's one possible implementation of such behaviour:

::

    class AddHeaderBehaviour(Behaviour):
        def __init__(self, behaviour, header_name, header_value):
            self._behaviour = behaviour
            self._header_name = header_name
            self._header_value = header_value

        def __call__(self, get_response, request):
            response = self._behaviour(get_response, request)
            response[self._header_name] = self._header_value

            return response

If you think that there's a use case that we haven't covered that might be useful for other users,
feel free to create an issue on `GitHub <https://github.com/abarto/django_uncertainty>`__.

Conditions
----------

Conditions are subclasses of the ``Predicate`` class:

::

    class Predicate:
        """Represents a condition that a Django request must meet. It is used in conjunction with
        ConditionalBehaviour to control if behaviours are invoked depending on the result of the
        Predicate invocation. Multiple predicates can be combined with or and and.
        """
        def __call__(self, get_response, request):
            """Returns True for all calls.
            :param get_response: The get_response method provided by the Django stack
            :param request: The request that triggered the middleware
            :return: True for all calls.
            """
            return True

Whenever a conditional behaviour is used, the predicate is invoked with the same parameters that
would be given the the behaviour.

is\_method
~~~~~~~~~~

The condition is met if the request uses the specified method.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.is_method('PATCH'), u.not_allowed())

is\_get
~~~~~~~

The condition is met if the request uses the GET HTTP method.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.is_get, u.not_allowed())

is\_delete
~~~~~~~~~~

The condition is met if the request uses the DELETE HTTP method.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.is_delete, u.not_allowed())

is\_post
~~~~~~~~

The condition is met if the request uses the POST HTTP method.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.is_post, u.not_allowed())

is\_put
~~~~~~~

The condition is met if the request uses the PUT HTTP method.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.is_put, u.not_allowed())

has\_parameter
~~~~~~~~~~~~~~

The condition is met if the request has the given parameter.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.has_parameter('q'), u.server_error())

has\_param
~~~~~~~~~~

An alias for ``has_parameter``

path\_matches
~~~~~~~~

The condition is met if the request path matches the given regular expression.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.path_matches('^/api'), u.delay(u.default(), 0.2))

is\_authenticated
~~~~~~~~~~~~~~~~~

The condition is met if the user has authenticated itself.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.is_authenticated, u.not_found())

user\_is
~~~~~~~~

The condition is met if the authenticated user has the given username.

::

    import uncertainty as u
    DJANGO_UNCERTAINTY = u.cond(u.user_is('admin', u.forbidden())

Custom conditions
~~~~~~~~~~~~~~~~~

As with behaviours, custom conditions are creating deriving the ``Predicate`` class. Let's say you
want a condition that checks the presence of a header in the request. Here's one possible
implementation of such condition:

::

    class HasHeaderPredicate(Predicate):
        def __index__(self, header_name):
            self._header_name = header_name

        def __call__(self, get_response, request):
            return self._header_name in request

Feedback
--------

All feedback is appreciated, so if you found problems or have ides for new features, just create an
issue on `GitHub <https://github.com/abarto/django_uncertainty>`_.
