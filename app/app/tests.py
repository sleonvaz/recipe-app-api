from django.test import TestCase

from app.app.calc import add


class CalcTest(TestCase):

    def test_add_numbers(self):
        """Test that two numbers are sum"""

        self.assertEqual(add(3, 8), 11)

