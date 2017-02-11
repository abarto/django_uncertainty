import re


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

    def __neg__(self):
        """The negation with another predicate
        :return: The negation of this predicate
        """
        return NotPredicate(self)

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


class NotPredicate(Predicate):
    def __init__(self, predicate):
        """The negation of a predicate.
        :param predicate: The predicate to negate
        """
        self._predicate = predicate

    def __call__(self, get_response, request):
        """Returns True if the predicate returns False
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if the predicate returns False and False otherwise
        """
        return not self._predicate(get_response, request)

    def __str__(self):
        return ('NotPredicate('
                'predicate={predicate})').format(predicate=self._predicate)


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
has_param = HasRequestParameterPredicate


class PathMatchesRegexpPredicate(Predicate):
    def __init__(self, regexp):
        """Checks if the request path matches the given regexp
        :param regexp: The regexp that the request path should match
        """
        self._regexp = re.compile(regexp)

    def __call__(self, get_response, request):
        """Returns True if the request path matches the regexp.
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if the request matches the regexp, False otherwise
        """
        return bool(self._regexp.match(request.path))

    def __str__(self):
        return 'PathMatchesRegexpPredicate(regexp={regexp})'.format(regexp=self._regexp)
path_matches = PathMatchesRegexpPredicate
path_is = path_matches


class IsAuthenticatedPredicate(Predicate):
    def __call__(self, get_response, request):
        """Returns True if the request is authenticated
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if the request is authenticated, False otherwise
        """
        return hasattr(request, 'user') and request.user.is_authenticated

    def __str__(self):
        return 'IsAuthenticatedPredicate()'
is_authenticated = IsAuthenticatedPredicate


class IsUserPredicate(Predicate):
    def __init__(self, username):
        """Checks if the request user username matches the given username
        :param username: The username that the request user should have
        """
        self._username = username

    def __call__(self, get_response, request):
        """Returns True if the request user username matches the given username
        :param get_response: The get_response method provided by the Django stack
        :param request: The request that triggered the middleware
        :return: True if the request user username matches the username, False otherwise
        """
        return hasattr(request, 'user') and request.user.username == self._username

    def __str__(self):
        return 'IsUser(username={username})'.format(username=self._username)
user_is = IsUserPredicate
