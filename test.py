"""
Unit tests
"""

import unittest

from pay_functions import week_pay, day_pay, worker_pay, validate_week_data

from config import message_strings, week_string_pattern


class TestPayFunction(unittest.TestCase):
    def test_week_pay(self):
        """Test week_pay function"""

        data = "MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        self.assertEqual(week_pay(data), 85.0)
        data = "MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        self.assertEqual(week_pay(data), 215.0)
        data = "MO00:00-22:00,TH01:00-13:00,SA14:00-18:00,SU20:00-00:00"
        self.assertEqual(week_pay(data), 880)

    def test_day_pay(self):
        """Test day pay function"""

        data = "MO10:00-12:00"
        self.assertEqual(day_pay(data), 30)
        data = "TH01:00-13:00"
        self.assertEqual(day_pay(data), 260)
        data = "SU20:00-21:00"
        self.assertEqual(day_pay(data), 25)
        data = "SA20:00-00:00"
        self.assertEqual(day_pay(data), 100)
        data = "TH08:00-20:00"
        self.assertEqual(day_pay(data), 200)

    def test_worker_pay(self):
        """Test worker pay function"""

        data = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        )
        name = data.split("=")[0]
        self.assertEqual(
            worker_pay(data), message_strings["amount_message"].format(name, 215.0)
        )
        data = "ROSE=MO00:00-22:00,TH01:00-13:00,SA14:00-18:00,SU02:00-23:30"
        name = data.split("=")[0]
        self.assertEqual(
            worker_pay(data), message_strings["amount_message"].format(name, 1307.5)
        )
        data = "JHON=MO00:00-09:00,TH09:00-18:00,SU18:00-00:00"
        name = data.split("=")[0]
        self.assertEqual(
            worker_pay(data), message_strings["amount_message"].format(name, 510.0)
        )

    def test_validate_week_data(self):
        """Test validate_week_data function"""

        data = "JHON=MO00:00-09:00,TH09:00-18:00,SU18:00-00:00"
        self.assertTrue(validate_week_data(data, week_string_pattern))
        data = "ROSE=MO00:00-22:00,TH01:00-13:00,SA14:00-18:00,SU02:00-23:30"
        self.assertTrue(validate_week_data(data, week_string_pattern))
        data = "ROSE=MO00:00-22:00,TH01:00-13:00,SA14:F0-18:00,SU02:00-23:30"
        self.assertFalse(validate_week_data(data, week_string_pattern))


if __name__ == "__main__":
    unittest.main()
