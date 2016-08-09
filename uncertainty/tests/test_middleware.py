from django.conf import settings
from django.test import TestCase, override_settings
from unittest.mock import MagicMock

from uncertainty.middleware import UncertaintyMiddleware


class UncertaintyMiddlewareTests(TestCase):
    def setUp(self):
        self.get_response_mock = MagicMock()
        self.request_mock = MagicMock()
        self.uncertainty_middleware = UncertaintyMiddleware(self.get_response_mock)

    @override_settings()
    def test_calls_get_response_if_setting_is_missing(self):
        """Tests that the middleware calls the given get_response if the DJANGO_UNCERTAINTY has not
        been set"""
        del settings.DJANGO_UNCERTAINTY
        self.uncertainty_middleware(self.request_mock)
        self.get_response_mock.assert_called_once_with(self.request_mock)

    @override_settings()
    def test_returns_get_response_result_if_setting_is_missing(self):
        """Tests that the middleware returns the result of calling get_response if the
        DJANGO_UNCERTAINTY has not been set"""
        del settings.DJANGO_UNCERTAINTY
        self.assertEqual(self.get_response_mock.return_value,
                         self.uncertainty_middleware(self.request_mock))

    @override_settings(DJANGO_UNCERTAINTY=None)
    def test_calls_get_response_if_setting_is_none(self):
        """Tests that the middleware calls the given get_response if the DJANGO_UNCERTAINTY setting
        is None"""
        self.uncertainty_middleware(self.request_mock)
        self.get_response_mock.assert_called_once_with(self.request_mock)

    @override_settings(DJANGO_UNCERTAINTY=None)
    def test_returns_get_response_result_if_setting_is_none(self):
        """Tests that the middleware returns the result of calling get_response if the
        DJANGO_UNCERTAINTY setting is None"""
        self.assertEqual(self.get_response_mock.return_value,
                         self.uncertainty_middleware(self.request_mock))

    def test_calls_django_uncertainty_setting(self):
        """Test that the middleware calls the DJANGO_UNCERTAINTY setting"""
        django_uncertainty = MagicMock()
        with self.settings(DJANGO_UNCERTAINTY=django_uncertainty):
            self.uncertainty_middleware(self.request_mock)
            django_uncertainty.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_returns_django_uncertainty_setting_result(self):
        """Test that the middleware returns the result of calling the DJANGO_UNCERTAINTY setting"""
        django_uncertainty = MagicMock()
        with self.settings(DJANGO_UNCERTAINTY=django_uncertainty):
            self.assertEqual(django_uncertainty.return_value,
                             self.uncertainty_middleware(self.request_mock))
