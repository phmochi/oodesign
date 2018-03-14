import unittest
from roulette import Wheel, PrisonOutcome

class TestEuroBinBuilder(unittest.TestCase):
    def setUp(self):
        self.wheel = Wheel(rules="european")
        
    def test_straight_bets(self):
        self.assertIsInstance(self.wheel.get_outcome("0"), PrisonOutcome)
        
    def test_five_bets(self):
        self.assertIsNone(self.wheel.get_outcome("00-0-1-2-3"))
        
    def test_four_bets(self):
        self.assertIsNotNone(self.wheel.get_outcome("0-1-2-3"))