from django.test import TestCase
from unittest.mock import MagicMock, patch

from uncertainty.conditions import Predicate


class PredicateTests(TestCase):
    def setUp(self):
        self.predicate = Predicate()
        self.other_predicate = MagicMock()

    def test_call_returns_true(self):
        """Test that invoking return True"""
        get_response_mock = MagicMock()
        request_mock = MagicMock()
        self.assertTrue(self.predicate(get_response_mock, request_mock))

    def test_negate_calls_not_predicate(self):
        """Test that negating the predicate calls NotPredicate"""
        with patch('uncertainty.conditions.NotPredicate') as not_predicate_mock:
            -self.predicate
            not_predicate_mock.assert_called_once_with(self.predicate)

    def test_negate_returns_not_predicate(self):
        """Test that negating the predicate returns a NotPredicate"""
        with patch('uncertainty.conditions.NotPredicate') as not_predicate_mock:
            self.assertEqual(not_predicate_mock.return_value, -self.predicate)

    def test_or_calls_or_predicate(self):
        """Test that using the bitwise or (|) operator with the predicate calls OrPredicate"""
        with patch('uncertainty.conditions.OrPredicate') as or_predicate_mock:
            self.predicate | self.other_predicate
            or_predicate_mock.assert_called_once_with(self.predicate, self.other_predicate)

    def test_or_returns_or_predicate(self):
        """Test that using the bitwise or (|) operator with the predicate a NotPredicate"""
        with patch('uncertainty.conditions.OrPredicate') as or_predicate_mock:
            self.assertEqual(or_predicate_mock.return_value, self.predicate | self.other_predicate)

    def test_and_calls_and_predicate(self):
        """Test that using the bitwise and (&) operator with the predicate calls OrPredicate"""
        with patch('uncertainty.conditions.AndPredicate') as and_predicate_mock:
            self.predicate & self.other_predicate
            and_predicate_mock.assert_called_once_with(self.predicate, self.other_predicate)

    def test_and_returns_and_predicate(self):
        """Test that using the bitwise and (&) operator with the predicate a NotPredicate"""
        with patch('uncertainty.conditions.AndPredicate') as and_predicate_mock:
            self.assertEqual(and_predicate_mock.return_value, self.predicate & self.other_predicate)

# TODO Add NotPredicate tests
# TODO Add OrPredicate tests
# TODO Add AndPredicate tests
# TODO Add IsMethodPredicate tests
# TODO Add is_get tests
# TODO Add is_delete tests
# TODO Add is_post tests
# TODO Add is_put tests
# TODO Add HasRequestParameterPredicate tests
# TODO Add PathMatchesRegexpPredicate tests
# TODO Add IsAuthenticatedPredicate tests
# TODO Add IsUserPredicate tests
