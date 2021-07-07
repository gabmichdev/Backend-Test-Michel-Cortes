from datetime import datetime

from django.test import TestCase

from core.utils.date_utils import generate_day_range_for_date, is_between


class DateUtilsTests(TestCase):
    """Class to test the date utils helper functions"""

    def test_is_between(self):
        """Test that values that are between return True"""
        date = datetime.now()
        gte = date.replace(hour=12)
        lte = date.replace(hour=23)
        self.assertTrue(is_between(left_value=0, value=1, right_value=2))
        self.assertTrue(is_between(left_value="0", value="1", right_value="2"))
        self.assertTrue(is_between(left_value=gte, value=date, right_value=lte))

    def test_non_comparable_values(self):
        """Test that comparing values that do not support comparison returns None"""
        self.assertIsNone(is_between(left_value=0, value=1, right_value="2"))

    def test_generate_daterange(self):
        """Test that the date is in the range generated"""
        date = datetime.now()
        gte, lte = generate_day_range_for_date(date)
        self.assertTrue(is_between(left_value=gte, value=date, right_value=lte))
