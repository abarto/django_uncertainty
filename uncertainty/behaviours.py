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
_default = default()


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


def not_found(*args, **kwargs):
    """A Behaviour that returns an HttpResponse object overriding the actual response of the Django
    stack with a 404 (Not found) status code. The function takes the same arguments as
    HttpResponse, which allows changing the content, status, or any other feature exposed through
    the constructor
    :param args: Positional arguments for the HttpResponse constructor
    :param kwargs: Named arguments for the HttpResponse constructor
    :return: An HttpResponse overriding the Django stack response
    """
    return HttpResponseBehaviour(HttpResponse, status=404, *args, **kwargs)


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
    :param data: A dictionary that is going to be serialized as JSON on the response
    :param args: Positional arguments for the JsonResponse constructor
    :param kwargs: Named arguments for the JsonResponse constructor
    :return: An JsonResponse overriding the Django stack response
    """
    return HttpResponseBehaviour(JsonResponse, data, *args, **kwargs)


class DelayResponseBehaviour(Behaviour):
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
delay = DelayResponseBehaviour


class DelayRequestBehaviour(Behaviour):
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
delay_request = DelayRequestBehaviour


class RandomChoiceBehaviour(Behaviour):
    def __init__(self, behaviours):
        """A behaviour that chooses randomly amongst the encapsulated behaviours. It is possible to
        specify different proportions between the behaviours. For instance, to specify a 50 percent
        of "Not Found" responses, 30 percent of "Server Error" responses and 20 percent of actual
        (that go through the Django stack) responses, you should use the following:

        RandomChoiceBehaviour([(not_found(), 0.5), (server_error(), 0.3), default())])

        If you just want a random choice between several behaviours, you can omit the proportion
        specification:

        RandomChoiceBehaviour([not_found, server_error, default])

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
        return _default(get_response, request)

    def __str__(self):
        return ('RandomChoiceBehaviour('
                'behaviours=[{behaviours}])').format(
                    behaviours=', '.join(b for b in self._behaviours))
random_choice = RandomChoiceBehaviour


class ConditionalBehaviour(Behaviour):
    def __init__(self, predicate, behaviour, alternative_behaviour=None):
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
        self._alternative_behaviour = alternative_behaviour or _default  # makes testing easier

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
cond = ConditionalBehaviour


class MultiConditionalBehaviour(Behaviour):
    def __init__(self, predicates_behaviours, default_behaviour=None):
        """A Behaviour that takes several conditions (predicates) and behaviours and executes the
        behaviour associated with the fist condition that is met. If no conditions are met,
        the supplied default behaviour is invoked.
        :param predicates_behaviours: A list of (predicate, behaviour) tuples
        :param default_behaviour: The default behaviour to invoke if no conditions are met
        """
        self._predicates_behaviours = predicates_behaviours
        self._default_behaviour = default_behaviour or _default  # makes testing easier

    def __call__(self, get_response, request):
        """It iterates through the conditions until one is met, and its associated behaviour is
        invoked and its result is returned. If no conditions are met the method returns the result
        of invoking the default behaviour.
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: The result of calling the behaviour that matches one of the conditions or the
        result of calling the default behaviour if no conditions are met.
        """

        for predicate, behaviour in self._predicates_behaviours:
            if predicate(get_response, request):
                return behaviour(get_response, request)

        return self._default_behaviour(get_response, request)

    def __str__(self, *args, **kwargs):
        return ('MultiConditionalBehaviour('
                'predicates_behaviours=[{predicates_behaviours}])'.format(
                    predicates_behaviours=', '.join(
                        '{p} -> {b}'.format(p=p, b=b) for p, b in self._predicates_behaviours)))
multi_conditional = MultiConditionalBehaviour
multi_cond = MultiConditionalBehaviour
case = MultiConditionalBehaviour


class StreamBehaviour(Behaviour):
    def wrap_streaming_content(self, streaming_content):
        """
        A generator that wraps the streaming content of the response returned get_response. Each
        chunk of the content is yielded. It is based on technique mentioned in
        https://docs.djangoproject.com/en/1.10/topics/http/middleware/#dealing-with-streaming-responses
        :param streaming_content: The streaming content of the response
        """
        for chunk in streaming_content:
            yield chunk

    def __call__(self, get_response, request):
        """If the response returned by get_response (as given by the UncertaintyMiddleware
        middleware is a streaming response, the streaming content is wrapped by the
        wrap_streaming_content generator. If the response is not a streaming one.
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: The result of calling get_response with the request parameter
        """
        response = get_response(request)

        if response.streaming:
            response.streaming_content = self.wrap_streaming_content(response.streaming_content)

        return response


class SlowdownStreamBehaviour(StreamBehaviour):
    def __init__(self, seconds):
        """A Behaviour that introduces a delay between each chunk of the streaming content
        returned by get_response.
        :param seconds: The amount of seconds to wait between each chunk of the streaming content
        """
        self._seconds = seconds

    def wrap_streaming_content(self, streaming_content):
        """Introduces a delay before yielding each chunk of streaming_content.
        :param streaming_content: The streaming_content field of the response.
        """
        for chunk in streaming_content:
            sleep(self._seconds)
            yield chunk

    def __str__(self):
        return ('SlowdownStreamBehaviour('
                'seconds={seconds})').format(seconds=self._seconds)
slowdown = SlowdownStreamBehaviour


class RandomStopStreamBehaviour(StreamBehaviour):
    def __init__(self, probability, stop_gracefully=True):
        """A Behaviour that stops the streaming with a certain probability.
        :param probability: The probability of stopping the stream
        """
        self._probability = probability

    def wrap_streaming_content(self, streaming_content):
        """Stops the iterator with with a certain probability.
        :param streaming_content: The streaming_content field of the response.
        """
        for chunk in streaming_content:
            if random() < self._probability:
                raise StopIteration()

            yield chunk

    def __str__(self):
        return ('RandomStopStreamBehaviour('
                'probability={probability},').format(probabilty=self._probability)
random_stop = RandomStopStreamBehaviour
