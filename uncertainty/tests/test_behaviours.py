from django.test import TestCase
from unittest.mock import MagicMock, patch

from uncertainty.behaviours import (Behaviour, default, HttpResponseBehaviour, html, ok,
                                    bad_request, forbidden, not_allowed, server_error, not_found,
                                    status, json, DelayResponseBehaviour, delay,
                                    DelayRequestBehaviour, delay_request, RandomChoiceBehaviour,
                                    cond, multi_conditional, StreamBehaviour, slowdown, random_stop)


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


class HttpResponseBehaviourTestsBase(TestCase):
    def setUp(self):
        http_response_behaviour_patcher = patch('uncertainty.behaviours.HttpResponseBehaviour')
        self.http_response_behaviour_mock = http_response_behaviour_patcher.start()
        self.addCleanup(http_response_behaviour_patcher.stop)
        self.args_mock = [MagicMock(), MagicMock()]
        self.kwargs_mock = {'kwarg0': MagicMock(), 'kwarg1': MagicMock()}


class HtmlTests(HttpResponseBehaviourTestsBase):
    def setUp(self):
        super().setUp()
        http_response_patcher = patch('uncertainty.behaviours.HttpResponse')
        self.http_response_mock = http_response_patcher.start()
        self.addCleanup(http_response_patcher.stop)

    def test_calls_http_response_behaviour(self):
        """Tests that html calls HttpResponseBehaviour with HttpResponse"""
        html(*self.args_mock, **self.kwargs_mock)
        self.http_response_behaviour_mock.assert_called_once_with(self.http_response_mock,
                                                                  *self.args_mock,
                                                                  **self.kwargs_mock)

    def test_returns_http_response_behaviour_result(self):
        """Tests that html returns the result of calling HttpResponseBehaviour constructor"""
        self.assertEqual(self.http_response_behaviour_mock.return_value,
                         html(*self.args_mock, **self.kwargs_mock))

    def test_ok_is_html(self):
        """Test that ok is an alias for html"""
        self.assertEqual(html, ok)


class BadRequestTests(HttpResponseBehaviourTestsBase):
        def setUp(self):
            super().setUp()
            http_response_bad_request_patcher = patch(
                'uncertainty.behaviours.HttpResponseBadRequest')
            self.http_response_bad_request_mock = http_response_bad_request_patcher.start()
            self.addCleanup(http_response_bad_request_patcher.stop)

        def test_calls_http_response_behaviour(self):
            """Tests that bad_request calls HttpResponseBehaviour with HttpResponseBadRequest"""
            bad_request(*self.args_mock, **self.kwargs_mock)
            self.http_response_behaviour_mock.assert_called_once_with(
                self.http_response_bad_request_mock, *self.args_mock, **self.kwargs_mock)

        def test_returns_http_response_behaviour_result(self):
            """Tests that bad_request returns the result of calling HttpResponseBehaviour
            constructor"""
            self.assertEqual(self.http_response_behaviour_mock.return_value,
                             bad_request(*self.args_mock, **self.kwargs_mock))


class ForbiddenTests(HttpResponseBehaviourTestsBase):
    def setUp(self):
        super().setUp()
        http_response_forbidden_patcher = patch(
            'uncertainty.behaviours.HttpResponseForbidden')
        self.http_response_forbidden_mock = http_response_forbidden_patcher.start()
        self.addCleanup(http_response_forbidden_patcher.stop)

    def test_calls_http_response_behaviour(self):
        """Tests that forbidden calls HttpResponseBehaviour with HttpResponseForbidden"""
        forbidden(*self.args_mock, **self.kwargs_mock)
        self.http_response_behaviour_mock.assert_called_once_with(
            self.http_response_forbidden_mock, *self.args_mock, **self.kwargs_mock)

    def test_returns_http_response_behaviour_result(self):
        """Tests that forbidden returns the result of calling HttpResponseBehaviour constructor"""
        self.assertEqual(self.http_response_behaviour_mock.return_value,
                         forbidden(*self.args_mock, **self.kwargs_mock))


class NotAllowedTests(HttpResponseBehaviourTestsBase):
    def setUp(self):
        super().setUp()
        http_response_not_allowed_patcher = patch(
            'uncertainty.behaviours.HttpResponseNotAllowed')
        self.http_response_not_allowed_mock = http_response_not_allowed_patcher.start()
        self.addCleanup(http_response_not_allowed_patcher.stop)

    def test_calls_http_response_behaviour(self):
        """Tests that not_allowed calls HttpResponseBehaviour with HttpResponseNotAllowed"""
        not_allowed(*self.args_mock, **self.kwargs_mock)
        self.http_response_behaviour_mock.assert_called_once_with(
            self.http_response_not_allowed_mock, *self.args_mock, **self.kwargs_mock)

    def test_returns_http_response_behaviour_result(self):
        """Tests that not_allowed returns the result of calling HttpResponseBehaviour constructor"""
        self.assertEqual(self.http_response_behaviour_mock.return_value,
                         not_allowed(*self.args_mock, **self.kwargs_mock))


class ServerErrorTests(HttpResponseBehaviourTestsBase):
    def setUp(self):
        super().setUp()
        http_response_server_error_patcher = patch(
            'uncertainty.behaviours.HttpResponseServerError')
        self.http_response_server_error_mock = http_response_server_error_patcher.start()
        self.addCleanup(http_response_server_error_patcher.stop)

    def test_calls_http_response_behaviour(self):
        """Tests that server_error calls HttpResponseBehaviour with HttpResponseNotAllowed"""
        server_error(*self.args_mock, **self.kwargs_mock)
        self.http_response_behaviour_mock.assert_called_once_with(
            self.http_response_server_error_mock, *self.args_mock, **self.kwargs_mock)

    def test_returns_http_response_behaviour_result(self):
        """Tests that server_error returns the result of calling HttpResponseServerError
        constructor"""
        self.assertEqual(self.http_response_behaviour_mock.return_value,
                         server_error(*self.args_mock, **self.kwargs_mock))


class NotFoundTests(HttpResponseBehaviourTestsBase):
    def setUp(self):
        super().setUp()
        http_response_patcher = patch('uncertainty.behaviours.HttpResponse')
        self.http_response_mock = http_response_patcher.start()
        self.addCleanup(http_response_patcher.stop)

    def test_calls_http_response_behaviour(self):
        """Tests that not_found calls HttpResponseBehaviour with HttpResponse"""
        not_found(*self.args_mock, **self.kwargs_mock)
        self.http_response_behaviour_mock.assert_called_once_with(self.http_response_mock,
                                                                  status=404,
                                                                  *self.args_mock,
                                                                  **self.kwargs_mock)

    def test_returns_http_response_behaviour_result(self):
        """Tests that not_found returns the result of calling HttpResponseBehaviour constructor"""
        self.assertEqual(self.http_response_behaviour_mock.return_value,
                         not_found(*self.args_mock, **self.kwargs_mock))


class StatusTests(HttpResponseBehaviourTestsBase):
    def setUp(self):
        super().setUp()
        http_response_patcher = patch('uncertainty.behaviours.HttpResponse')
        self.http_response_mock = http_response_patcher.start()
        self.addCleanup(http_response_patcher.stop)
        self.some_status = MagicMock()

    def test_calls_http_response_behaviour(self):
        """Tests that status calls HttpResponseBehaviour with HttpResponse"""
        status(self.some_status, *self.args_mock, **self.kwargs_mock)
        self.http_response_behaviour_mock.assert_called_once_with(self.http_response_mock,
                                                                  status=self.some_status,
                                                                  *self.args_mock,
                                                                  **self.kwargs_mock)

    def test_returns_http_response_behaviour_result(self):
        """Tests that status returns the result of calling HttpResponseBehaviour constructor"""
        self.assertEqual(self.http_response_behaviour_mock.return_value,
                         status(self.some_status, *self.args_mock, **self.kwargs_mock))


class JsonTests(HttpResponseBehaviourTestsBase):
    def setUp(self):
        super().setUp()
        json_response_patcher = patch('uncertainty.behaviours.JsonResponse')
        self.json_response_mock = json_response_patcher.start()
        self.addCleanup(json_response_patcher.stop)
        self.some_data = MagicMock()

    def test_calls_http_response_behaviour(self):
        """Tests that json calls HttpResponseBehaviour with JsonResponse"""
        json(self.some_data, *self.args_mock, **self.kwargs_mock)
        self.http_response_behaviour_mock.assert_called_once_with(
            self.json_response_mock, self.some_data, *self.args_mock, **self.kwargs_mock)

    def test_returns_http_response_behaviour_result(self):
        """Tests that json returns the result of calling JsonResponse constructor"""
        self.assertEqual(self.http_response_behaviour_mock.return_value,
                         json(self.some_data, *self.args_mock, **self.kwargs_mock))


class DelayResponseBehaviourTests(TestCase):
    def setUp(self):
        sleep_patcher = patch('uncertainty.behaviours.sleep')
        self.sleep_mock = sleep_patcher.start()
        self.addCleanup(self.sleep_mock.stop)
        self.get_response_mock = MagicMock()
        self.request_mock = MagicMock()
        self.some_behaviour = MagicMock()
        self.some_seconds = MagicMock()
        self.delay_response_behaviour = DelayResponseBehaviour(self.some_behaviour,
                                                               self.some_seconds)

    def test_calls_encapsulated_behaviour(self):
        """Tests that DelayResponseBehaviour calls the encapsulated behaviour"""
        self.delay_response_behaviour(self.get_response_mock, self.request_mock)
        self.some_behaviour.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_returns_result_of_encapsulated_behaviour(self):
        """Tests that DelayResponseBehaviour returns the result of calling the encapsulated
        behaviour"""
        self.assertEqual(self.some_behaviour.return_value,
                         self.delay_response_behaviour(self.get_response_mock, self.request_mock))

    def test_calls_sleep(self):
        """Tests that DelayResponseBehaviour calls sleep for the given seconds"""
        self.delay_response_behaviour(self.get_response_mock, self.request_mock)
        self.sleep_mock.assert_called_once_with(self.some_seconds)

    def test_delay_is_delay_response_behaviour(self):
        """Tests that delay is an alias for DelayResponseBehaviour"""
        self.assertEqual(delay, DelayResponseBehaviour)


class DelayRequestBehaviourTests(TestCase):
    def setUp(self):
        sleep_patcher = patch('uncertainty.behaviours.sleep')
        self.sleep_mock = sleep_patcher.start()
        self.addCleanup(self.sleep_mock.stop)
        self.get_response_mock = MagicMock()
        self.request_mock = MagicMock()
        self.some_behaviour = MagicMock()
        self.some_seconds = MagicMock()
        self.delay_request_behaviour = DelayRequestBehaviour(self.some_behaviour,
                                                             self.some_seconds)

    def test_calls_encapsulated_behaviour(self):
        """Tests that DelayResponseBehaviour calls the encapsulated behaviour"""
        self.delay_request_behaviour(self.get_response_mock, self.request_mock)
        self.some_behaviour.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_returns_result_of_encapsulated_behaviour(self):
        """Tests that DelayResponseBehaviour returns the result of calling the encapsulated
        behaviour"""
        self.assertEqual(self.some_behaviour.return_value,
                         self.delay_request_behaviour(self.get_response_mock,
                                                      self.request_mock))

    def test_calls_sleep(self):
        """Tests that DelayResponseBehaviour calls sleep for the given seconds"""
        self.delay_request_behaviour(self.get_response_mock, self.request_mock)
        self.sleep_mock.assert_called_once_with(self.some_seconds)

    def test_delay_is_delay_request_response_behaviour(self):
        """Tests that delay is an alias for DelayResponseBehaviour"""
        self.assertEqual(delay_request, DelayRequestBehaviour)


class RandomChoiceBehaviourInitTests(TestCase):
    def setUp(self):
        self.behaviour_0 = MagicMock()
        self.behaviour_1 = MagicMock()
        self.behaviour_2 = MagicMock()

    def test_value_error_raised_on_proportions_sum_over_1(self):
        """Tests that if the sum of the specified proportions is greater than 1, a ValueError
        exception is raised"""
        self.assertRaises(ValueError, RandomChoiceBehaviour,
                          ((self.behaviour_0, 0.5), (self.behaviour_0, 0.6)))
        self.assertRaises(ValueError, RandomChoiceBehaviour, ((self.behaviour_0, 1.2),))

    def test_behaviours_with_no_proportions_evenly_distributed(self):
        """Tests that behaviours with no proportions are evenly distributed"""
        random_choice = RandomChoiceBehaviour((self.behaviour_0, self.behaviour_1))
        self.assertEqual(0.5, random_choice._behaviours[0][1])
        self.assertEqual(1.0, random_choice._behaviours[1][1])

    def test_behaviours_with_no_proportions_evenly_distributes_rest(self):
        """Tests that if there are behaviours with proportions and behaviours with no proportions,
        the latter are evenly distributed"""
        random_choice = RandomChoiceBehaviour(((self.behaviour_0, 0.5), self.behaviour_1,
                                               self.behaviour_2))
        self.assertEqual(0.5, random_choice._behaviours[0][1])
        self.assertEqual(0.75, random_choice._behaviours[1][1])
        self.assertEqual(1.0, random_choice._behaviours[2][1])

    def test_proportions_are_accumulated(self):
        """Tests that proportions accumulate in a CDF fashion"""
        random_choice = RandomChoiceBehaviour(((self.behaviour_0, 0.3), (self.behaviour_1, 0.2),
                                               (self.behaviour_2, 0.1)))
        self.assertTupleEqual((self.behaviour_0, 0.3), random_choice._behaviours[0])
        self.assertTupleEqual((self.behaviour_1, 0.5), random_choice._behaviours[1])
        self.assertTupleEqual((self.behaviour_2, 0.6), random_choice._behaviours[2])


class RandomChoiceBehaviourTests(TestCase):
    def setUp(self):
        random_patcher = patch('uncertainty.behaviours.random')
        self.random_mock = random_patcher.start()
        self.addCleanup(self.random_mock.stop)
        default_patcher = patch('uncertainty.behaviours._default')
        self.default_mock = default_patcher.start()
        self.addCleanup(self.default_mock.stop)

        self.get_response_mock = MagicMock()
        self.request_mock = MagicMock()

        self.behaviour_0 = MagicMock()
        self.behaviour_1 = MagicMock()
        self.behaviour_2 = MagicMock()
        self.behaviour_0_prop = (self.behaviour_0, 0.2)
        self.behaviour_1_prop = (self.behaviour_1, 0.3)
        self.behaviour_2_prop = (self.behaviour_2, 0.1)

        self.random_choice = RandomChoiceBehaviour(
            (self.behaviour_0_prop, self.behaviour_1_prop, self.behaviour_2_prop))

    def test_behaviour_0_invoked_if_random_is_zero(self):
        """Tests that if the random number is 0, behaviour_0 is invoked"""
        self.random_mock.return_value = 0
        self.random_choice(self.get_response_mock, self.request_mock)
        self.behaviour_0.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_behaviour_0_invoked_if_random_less_than_0_2(self):
        """Tests that if the random number is less than 0.2, behaviour_0 is invoked"""
        self.random_mock.return_value = 0.1
        self.random_choice(self.get_response_mock, self.request_mock)
        self.behaviour_0.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_behaviour_1_invoked_if_random_is_0_2(self):
        """Tests that if the random number is exactly 0.2, behaviour_1 is invoked"""
        self.random_mock.return_value = 0.2
        self.random_choice(self.get_response_mock, self.request_mock)
        self.behaviour_1.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_behaviour_1_invoked_if_random_less_than_0_5(self):
        """Tests that if the random number is less than 0.5, behaviour_1 is invoked"""
        self.random_mock.return_value = 0.45
        self.random_choice(self.get_response_mock, self.request_mock)
        self.behaviour_1.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_behaviour_2_invoked_if_random_is_0_5(self):
        """Tests that if the random number is exactly 0.5, behaviour_2 is invoked"""
        self.random_mock.return_value = 0.5
        self.random_choice(self.get_response_mock, self.request_mock)
        self.behaviour_2.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_behaviour_2_invoked_if_random_less_than_0_6(self):
        """Tests that if the random number is less than 0.6, behaviour_2 is invoked"""
        self.random_mock.return_value = 0.57
        self.random_choice(self.get_response_mock, self.request_mock)
        self.behaviour_2.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_default_invoked_if_random_is_0_6(self):
        """Tests that if the random number is exactly 0.6, the default behaviour is invoked"""
        self.random_mock.return_value = 0.6
        self.random_choice(self.get_response_mock, self.request_mock)
        self.default_mock.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_default_invoked_if_random_greater_than_0_6(self):
        """Tests that if the random number is greater than 0.6, the default behaviour is invoked"""
        self.random_mock.return_value = 0.7
        self.random_choice(self.get_response_mock, self.request_mock)
        self.default_mock.assert_called_once_with(self.get_response_mock, self.request_mock)


class ConditionalBehaviourTests(TestCase):
    def setUp(self):
        default_patcher = patch('uncertainty.behaviours._default')
        self.default_mock = default_patcher.start()
        self.addCleanup(self.default_mock.stop)

        self.get_response_mock = MagicMock()
        self.request_mock = MagicMock()

        self.predicate = MagicMock()
        self.behaviour = MagicMock()
        self.alternative_behaviour = MagicMock()

        self.cond = cond(self.predicate, self.behaviour, self.alternative_behaviour)

    def test_behaviour_invoked_predicate_true(self):
        """Tests that if the predicate is True, behaviour is invoked"""
        self.predicate.return_value = True
        self.cond(self.get_response_mock, self.request_mock)
        self.behaviour.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_returns_behaviour_result_predicate_true(self):
        """Test that if the predicate is True, the result of invoking behaviour is returned"""
        self.predicate.return_value = True
        response = self.cond(self.get_response_mock, self.request_mock)
        self.assertEqual(self.behaviour.return_value, response)

    def test_behaviour_not_invoked_predicate_false(self):
        """Tests that if the predicate is False, behaviour is not invoked"""
        self.predicate.return_value = False
        self.cond(self.get_response_mock, self.request_mock)
        self.assertFalse(self.behaviour.called)

    def test_returns_alternative_behaviour_result_predicate_true(self):
        """Test that if the predicate is False, the result of invoking alternative_behaviour is
        returned"""
        self.predicate.return_value = False
        response = self.cond(self.get_response_mock, self.request_mock)
        self.assertEqual(self.alternative_behaviour.return_value, response)

    def test_alternate_behaviour_invoked_predicate_false(self):
        """Tests that if the predicate is False, alternate_behaviour is invoked"""
        self.predicate.return_value = False
        self.cond(self.get_response_mock, self.request_mock)
        self.alternative_behaviour.assert_called_once_with(self.get_response_mock,
                                                           self.request_mock)

    def test_default_invoked_predicate_false(self):
        """Tests that if the predicate is False, and no alternate_behaviour is provided, default is
        invoked"""
        self.predicate.return_value = False
        cond_ = cond(self.predicate, self.behaviour)
        cond_(self.get_response_mock, self.request_mock)
        self.default_mock.assert_called_once_with(self.get_response_mock, self.request_mock)

    def test_returns_default_result_predicate_false(self):
        """Tests that if the predicate is False, and no alternate_behaviour is provided, the result
        of invoking default is returned"""
        self.predicate.return_value = False
        cond_ = cond(self.predicate, self.behaviour)
        cond_(self.get_response_mock, self.request_mock)
        response = cond_(self.get_response_mock, self.request_mock)
        self.assertEqual(self.default_mock.return_value, response)


# TODO Add ConditionalBehaviour tests
# TODO Add MultiConditionalBehaviour tests
# TODO Add StreamBehaviour tests
# TODO Add SlowdownStreamBehaviour tests
# TODO Add RandomStopStreamBehaviour tests
