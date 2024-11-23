import unittest

from django.test import TestCase
from etl.utils import convert_currency


class TestUtils(TestCase):
    def test_convert_currency_same_currency(self):
        result = convert_currency(100.0, "USD", "USD")
        self.assertEqual(result, 100.0)

    def test_convert_currency_different_currency(self):
        result = convert_currency(100.0, "USD", "EUR")
        self.assertGreater(result, 0.0)
        self.assertNotEqual(result, 100.0)
        self.assertEqual(result, 91.0)


if __name__ == "__main__":
    unittest.main()
