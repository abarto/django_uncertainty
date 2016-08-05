from random import random
from time import sleep

from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden,
                         HttpResponseNotAllowed, HttpResponseServerError, JsonResponse)


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
default = Behaviour


class HttpResponseBehaviour(Behaviour):
    def __init__(self, response_class, *args, **kwargs):
        """A Behaviour that overrides the default response with the result of calling an
        HttpResponse constructor.
        :param response_class: An HttpResponse class
        :param args: The positional arguments for the HttpResponse constructor
        :param kwargs: The named arguments for the HttpResponse constructor
        """
        self._response_class = response_class
        self._args = args
        self._kwargs = kwargs

    def __call__(self, get_response, request):
        """Returns the result of calling the HttpResponse constructor with the positional and named
        arguments supplied. The get_response method provided by the Django stack is never called.
        :param get_response: The get_response method provided by the Django stack (ignored)
        :param request: The request that triggered the middleware (ignored)
        :return: The result of calling the HttpResponse constructor with the positional and named
        arguments supplied.
        """
        response = self._response_class(*self._args, **self._kwargs)
        return response

    def __str__(self):
        return ('HttpResponseBehaviour('
                'response_class={response_class}, '
                'args={args}, '
                'kwargs={kwargs})').format(response_class=self._response_class,
                                           args=self._args,
                                           kwargs=self._kwargs)


def html(*args, **kwargs):
    """A Behaviour that returns an HttpResponse object overriding the actual response of the Django
    stack. The function takes the same arguments as HttpResponse, which allows changing the content,
    status, or any other feature exposed through the constructor
    :param args: Positional arguments for the HttpResponse constructor
    :param kwargs: Named arguments for the HttpResponse constructor
    :return: An HttpResponse overriding the Django stack response
    """
    return HttpResponseBehaviour(HttpResponse, *args, **kwargs)
ok = html


def bad_request(*args, **kwargs):
    """A Behaviour that returns an HttpResponseBadRequest object overriding the actual response of
    the Django stack. The function takes the same arguments as HttpResponseBadRequest, which allows
    changing the content, status, or any other feature exposed through the constructor
    :param args: Positional arguments for the HttpResponseBadRequest constructor
    :param kwargs: Named arguments for the HttpResponseBadRequest constructor
    :return: An HttpResponseBadRequest overriding the Django stack response
    """
    return HttpResponseBehaviour(HttpResponseBadRequest, *args, **kwargs)


def forbidden(*args, **kwargs):
    """A Behaviour that returns an HttpResponseForbidden object overriding the actual response of
    the Django stack. The function takes the same arguments as HttpResponseForbidden, which allows
    changing the content, status, or any other feature exposed through the constructor
    :param args: Positional arguments for the HttpResponseForbidden constructor
    :param kwargs: Named arguments for the HttpResponseForbidden constructor
    :return: An HttpResponseForbidden overriding the Django stack response
    """
    return HttpResponseBehaviour(HttpResponseForbidden, *args, **kwargs)


def not_allowed(*args, **kwargs):
    """A Behaviour that returns an HttpResponseNotAllowed object overriding the actual response of
    the Django stack. The function takes the same arguments as HttpResponseNotAllowed, which allows
    changing the content, status, or any other feature exposed through the constructor
    :param args: Positional arguments for the HttpResponseNotAllowed constructor
    :param kwargs: Named arguments for the HttpResponseNotAllowed constructor
    :return: An HttpResponseNotAllowed overriding the Django stack response
    """
    return HttpResponseBehaviour(HttpResponseNotAllowed, *args, **kwargs)


def server_error(*args, **kwargs):
    """A Behaviour that returns an HttpResponseServerError object overriding the actual response of
    the Django stack. The function takes the same arguments as HttpResponseServerError, which allows
    changing the content, status, or any other feature exposed through the constructor
    :param args: Positional arguments for the HttpResponseServerError constructor
    :param kwargs: Named arguments for the HttpResponseServerError constructor
    :return: An HttpResponseServerError overriding the Django stack response
    """
    return HttpResponseBehaviour(HttpResponseServerError, *args, **kwargs)


def status(status_code, *args, **kwargs):
    """A Behaviour that returns an HttpResponse object overriding the actual response of the Django
    stack with a specific status code. The function takes the same arguments as HttpResponse, which
    allows changing the content, status, or any other feature exposed through the constructor
    :param status_code: The status code of the response.
    :param args: Positional arguments for the HttpResponse constructor
    :param kwargs: Named arguments for the HttpResponse constructor
    :return: An HttpResponse overriding the Django stack response
    """
    return HttpResponseBehaviour(HttpResponse, status=status_code, *args, **kwargs)


def json(data, *args, **kwargs):
    """A Behaviour that returns an JsonResponse object overriding the actual response of the Django
    stack. The function takes the same arguments as JsonResponse, which allows changing the content,
    status, or any other feature exposed through the constructor
    :param args: Positional arguments for the JsonResponse constructor
    :param kwargs: Named arguments for the JsonResponse constructor
    :return: An JsonResponse overriding the Django stack response
    """
    return HttpResponseBehaviour(JsonResponse, data, *args, **kwargs)


class DelayResponse(Behaviour):
    def __init__(self, behaviour, seconds):
        """A Behaviour that delays the response to the client a given amount of seconds.
        :param behaviour: The behaviour to invoke before delaying its response
        :param seconds: The amount of seconds to wait after requesting a response from the behaviour
        """
        self._behaviour = behaviour
        self._seconds = seconds

    def __call__(self, get_response, request):
        """Returns the result of invoking the encapsulated behaviour using the parameters given by
        the Django middleware after waiting for a given amount of seconds. The get_response method
        provided by the Django stack is never called.
        :param get_response: The get_response method provided by the Django stack (ignored)
        :param request: The request that triggered the middleware (ignored)
        :return: The result of calling the encapsulated behaviour
        """
        response = self._behaviour(get_response, request)
        sleep(self._seconds)
        return response

    def __str__(self):
        return ('DelayResponse('
                'behaviour={behaviour}, '
                'seconds={seconds})').format(behaviour=self._behaviour,
                                             seconds=self._seconds)
delay = DelayResponse


class DelayRequest(Behaviour):
    def __init__(self, behaviour, seconds):
        """A Behaviour that delays the response to the client a given amount of seconds. It
        introduces the delay BEFORE invoking the encapsulated behaviour.
        :param behaviour: The behaviour to invoke
        :param seconds: The amount of seconds to wait before requesting a response from the
        behaviour
        """
        self._behaviour = behaviour
        self._seconds = seconds

    def __call__(self, get_response, request):
        """It waits a given amount of seconds and returns the result of invoking the encapsulated
        behaviour using the parameters given by the Django middleware. The get_response method
        provided by the Django stack is never called.
        :param get_response: The get_response method provided by the Django stack (ignored)
        :param request: The request that triggered the middleware (ignored)
        :return: The result of calling the encapsulated behaviour
        """
        sleep(self._seconds)
        response = self._behaviour(get_response, request)
        return response

    def __str__(self):
        return ('DelayRequest('
                'behaviour={behaviour}, '
                'seconds={seconds})').format(behaviour=self._behaviour,
                                             seconds=self._seconds)
delay_request = DelayRequest


class RandomChoice(Behaviour):
    def __init__(self, behaviours):
        """A behaviour that chooses randomly amongst the encapsulated behaviours. It is possible to
        specify different proportions between the behaviours. For instance, to specify a 50 percent
        of "Not Found" responses, 30 percent of "Server Error" responses and 20 percent of actual
        (that go through the Django stack) responses, you should use the following:

        RandomChoice([(not_found(), 0.5), (server_error(), 0.3), default())])

        If you just want a random choice between several behaviours, you can omit the proportion
        specification:

        RandomChoice([not_found, server_error, default])

        :param behaviours: A sequence of Behaviour objects or tuples of a Behaviour object and a
        number less than 1 representing the proportion of requests that are going to exhibit that
        behaviour.
        """
        self._behaviours = self._init_cdf(behaviours)

    def _init_cdf(self, behaviours):
        with_proportions = list(filter(lambda s: isinstance(s, (list, tuple)), behaviours))
        without_proportions = list(filter(lambda s: not isinstance(s, (list, tuple)), behaviours))

        sum_with_proportions = sum(s[1] for s in with_proportions)
        if sum_with_proportions > 1 or (sum_with_proportions == 1 and len(without_proportions) > 0):
            raise ValueError('The sum of the behaviours proportions is greater than 1')

        if len(without_proportions) > 0:
            proportion = (1 - sum_with_proportions) / len(without_proportions)
            for behaviour in without_proportions:
                with_proportions.append((behaviour, proportion))

        cum_sum = 0
        cdf = []
        for behaviour, proportion in with_proportions:
            cum_sum += proportion
            cdf.append((behaviour, cum_sum))

        return cdf

    def __call__(self, get_response, request):
        """Returns the result of invoking the a randomly chosen behaviour using the parameters
        given by the Django middleware. The get_response method provided by the Django stack is
        never called.
        :param get_response: The get_response method provided by the Django stack (ignored)
        :param request: The request that triggered the middleware (ignored)
        :return: The result of calling one of the encapsulated behaviours chosing randomly amognst
        them.
        """
        x = random()
        for behaviour, f_x in self._behaviours:
            if x < f_x:
                return behaviour(get_response, request)
        return default(get_response, request)

    def __str__(self):
        return ('RandomChoice('
                'behaviours=[{behaviours}])').format(
                    behaviours=', '.join(b for b in self._behaviours))
random_choice = RandomChoice


class ConditionalBehaviour(Behaviour):
    def __init__(self, predicate, behaviour, alternative_behaviour=default):
        """A Behaviour that invokes the encapsulated behaviour if a condition is met, otherwise it
        invokes the alternative behaviour. The default alternative behaviour is just going through
        the usual middleware path.
        :param predicate: The Predicate to invoke to determine if the condition is met
        :param behaviour: The behaviour to invoke if the condition is met
        :param alternative_behaviour: The alternative behaviour to invoke if the condition is not
        met
        """
        self._predicate = predicate
        self._behaviour = behaviour
        self._alternative_behaviour = alternative_behaviour

    def __call__(self, get_response, request):
        """If the predicate condition is met it returns the result of invoking the encapsulated
        behaviour using the parameters given by the Django middleware. If the condition is not met,
        the alternative behaviour is invoked (with the usual parameters).
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: The result of calling the encapsulated behaviour if the predicate condition is met
        or the result of invoking the alternative behaviour otherwise.
        """
        if self._predicate(get_response, request):
            return self._behaviour(get_response, request)

        return self._alternative_behaviour(get_response, request)

    def __str__(self):
        return ('ConditionalBehaviour('
                'predicate={predicate}, '
                'behaviour={behaviour}, '
                'alternative_behaviour={alternative_behaviour})').format(
                    predicate=self._predicate, behaviour=self._behaviour,
                    alternative_behaviour=self._alternative_behaviour)
conditional = ConditionalBehaviour


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

    def __or__(self, other):
        """The disjunction with another predicate
        :param other: The other predicate
        :return: A disjunction between this predicate and another
        """
        return OrPredicate(self, other)

    def __and__(self, other):
        """The conjunction with another predicate
        :param other: The other predicate
        :return: A conjunction between this predicate and another
        """
        return AndPredicate(self, other)

    def __str__(self):
        return 'Predicate(True)'


class OrPredicate(Predicate):
    def __init__(self, left, right):
        """The disjunction of two predicates.
        :param left: The left predicate
        :param right: The right predicate
        """
        self._left = left
        self._right = right

    def __call__(self, get_response, request):
        """Returns True if either predicate calls return True
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if either predicate calls is True, False otherwise
        """
        return self._left(get_response, request) or self._right(get_response, request)

    def __str__(self):
        return ('OrPredicate('
                'left={left}, '
                'right={right})').format(left=self._left, right=self._right)


class AndPredicate(Predicate):
    def __init__(self, left, right):
        """The conjunction of two predicates.
        :param left: The left predicate
        :param right: The right predicate
        """
        self._left = left
        self._right = right

    def __call__(self, get_response, request):
        """Returns True if both predicate calls return True
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if both predicate calls is True, False otherwise
        """
        return self._left(get_response, request) and self._right(get_response, request)

    def __str__(self):
        return ('AndPredicate('
                'left={left}, '
                'right={right})').format(left=self._left, right=self._right)


class IsMethodPredicate(Predicate):
    def __init__(self, method):
        """Checks if the request method is the same as the one provided.
        :param method: The HTTP method (GET, POST, etc.) that request.method ought to be equal to
        """
        self._method = method

    def __call__(self, get_response, request):
        """Returns True if the request uses the encapsulated HTTP method.
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if the request uses the encapuslated method, False otherwise.
        """
        return request.method == self._method

    def __str__(self):
        return ('IsMethodPredicate('
                'method={method})').format(method=self._method)
is_method = IsMethodPredicate
is_get = IsMethodPredicate('GET')
is_delete = IsMethodPredicate('DELETE')
is_post = IsMethodPredicate('POST')
is_put = IsMethodPredicate('PUT')


class HasRequestParameterPredicate(Predicate):
    def __init__(self, parameter):
        """Checks if the request contains a parameter.
        :param parameter: The name of the parameters
        """
        self._parameter = parameter

    def __call__(self, get_response, request):
        """Returns True if the request has a parameter
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if the request has a parameter, False otherwise
        """
        return self._parameter in request.GET or self._parameter in request.POST

    def __str__(self):
        return ('HasRequestParameterPredicate('
                'parameter={parameter})').format(parameter=self._parameter)
has_parameter = HasRequestParameterPredicate
