"""
Unit tests
"""

import unittest

from pay_functions import week_pay, day_pay


class TestPayFunction(unittest.TestCase):
    def test_pay(self):
        # Test case with a sample input
        data = "MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        self.assertAlmostEqual(week_pay(data), 85.0)
        data = "MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        self.assertAlmostEqual(week_pay(data), 215.0)
        data = "MO00:00-22:00,TH01:00-13:00,SA14:00-18:00,SU20:00-00:00"
        self.assertAlmostEqual(week_pay(data), 880)

    def test_day_pay(self):
        pass


if __name__ == '__main__':
    unittest.main()
