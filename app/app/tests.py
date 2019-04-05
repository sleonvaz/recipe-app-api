from django.test import TestCase

from app.calc import add, subtracts


class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that values are added together"""
        self.assertEqual(add(3, 8), 11)

    def test_subtract_numbers(self):
        """ Test that the values are subtracted and returned"""
        self.assertEquals(subtracts(5, 11),6)
