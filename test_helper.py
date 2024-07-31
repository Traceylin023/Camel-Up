import unittest
from helper import *

class HelperTest(unittest.TestCase):
    def test_number_colors(self):
        """Make sure we have the right number of colors"""
        self.assertEqual(len(Color), 5) # we have 5 colors: red, yellow, green, blue, and purple 

    def test_ticket_equality(self):
        self.assertEqual(BettingTicket(Color.purple, 5), BettingTicket(Color.purple, 5))

    def test_ticket_mismatched_colors(self):
        self.assertNotEqual(BettingTicket(Color.blue, 5), BettingTicket(Color.yellow, 5))

    def test_ticket_mismatched_values(self):
        self.assertNotEqual(BettingTicket(Color.purple, 3), BettingTicket(Color.purple, 5))

    def test_ticket_invalid_value(self):
        self.assertRaises(AssertionError, BettingTicket, Color.yellow, 10)

    def test_camel_get_color(self):
        self.assertEqual(Camel(Color.purple).get_color(), Color.purple)

    def test_camel_get_invalid_color(self):
        self.assertNotEqual(Camel(Color.yellow).get_color(), Color.green)

    def test_camel_equality(self):
        """Make sure camels are equal by color."""
        self.assertEqual(Camel(Color.red), Camel(Color.red))
        self.assertNotEqual(Camel(Color.green), Camel(Color.blue))

if __name__ == '__main__':
    unittest.main()
