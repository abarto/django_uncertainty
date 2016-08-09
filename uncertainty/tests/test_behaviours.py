from django.test import TestCase
from unittest.mock import MagicMock

from uncertainty.behaviours import Behaviour, default, HttpResponseBehaviour


class BehaviourTests(TestCase):
    def setUp(self):
        self.get_response_mock = MagicMock()
        self.request_mock = MagicMock()
        self.behaviour = Behaviour()

    def test_calls_get_response(self):
        """Tests that invoking the behaviour calls get_response"""
        self.behaviour(self.get_response_mock, self.request_mock)
        self.get_response_mock.assert_called_once_with(self.request_mock)

    def test_returns_get_response_result(self):
        """Tests that the behaviour returns the result of calling get_response"""
        self.assertEqual(self.get_response_mock.return_value,
                         self.behaviour(self.get_response_mock, self.request_mock))


class DefaultTests(TestCase):
    def test_default_is_behaviour_base(self):
        """Test that default is the Behaviour base class"""
        self.assertEqual(default, Behaviour)


class HttpResponseBehaviourTests(TestCase):
    def setUp(self):
        self.get_response_mock = MagicMock()
        self.request_mock = MagicMock()
        self.response_class_mock = MagicMock()
        self.args_mock = [MagicMock(), MagicMock()]
        self.kwargs_mock = {'kwarg0': MagicMock(), 'kwarg1': MagicMock()}
        self.behaviour = HttpResponseBehaviour(self.response_class_mock, *self.args_mock,
                                               **self.kwargs_mock)

    def test_calls_response_class_constructor(self):
        """Tests that invoking the behaviour calls response class constructor"""
        self.behaviour(self.get_response_mock, self.request_mock)
        self.response_class_mock.assert_called_once_with(*self.args_mock, **self.kwargs_mock)

    def test_returns_response_class_constructor_result(self):
        """Tests that the behaviour returns the result of calling the response class constructor"""
        self.assertEqual(self.response_class_mock.return_value,
                         self.behaviour(self.get_response_mock, self.request_mock))

# TODO Add html tests
# TODO Add bad_request tests
# TODO Add forbidden tests
# TODO Add not_allowed tests
# TODO Add server_error tests
# TODO Add not_found tests
# TODO Add status tests
# TODO Add json tests
# TODO Add DelayResponse tests
# TODO Add DelayRequest tests
# TODO Add RandomChoice tests
# TODO Add ConditionalBehaviour tests
# TODO Add MultiConditionalBehaviour tests
