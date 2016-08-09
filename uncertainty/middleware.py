from django.conf import settings


class UncertaintyMiddleware(object):
    def __init__(self, get_response):
        """A Django middleware to introduced controlled uncertainty into the stack. It is controlled
        by the DJANGO_UNCERTAINTY setting, were the developers can specify (using the provided
        behaviours or their own) the way Django should respond depending on certain conditions. For
        example, if you want Django to respond with a server_error 30% of the time, but only
        if the requests are POST or PUT, you can use the following specification:

        DJANGO_UNCERTAINTY = random_choice([(conditional(is_post or is_put, server_error()), 0.3)])

        :param get_response: The get_response method provided by the Django stack
        """
        self.get_response = get_response

    def __call__(self, request):
        """Controls the middleware behaviour using the specification given by the DJANGO_UNCERTAINTY
        setting.
        :param request: The request provided by the Django stack
        :return: The result of running the uncertainty specification if the DJANGO_UNCERTAINTY is
        present, or the default response if it's not.
        """
        if hasattr(settings, 'DJANGO_UNCERTAINTY') and settings.DJANGO_UNCERTAINTY is not None:
            return settings.DJANGO_UNCERTAINTY(self.get_response, request)

        return self.get_response(request)
