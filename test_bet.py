import unittest
from roulette import Bet, Outcome

class TestBet(unittest.TestCase):
    def test_win_amount(self):
        o1 = Outcome("0",35)
        b1 = Bet(5, o1)
        self.assertEqual(b1.win_amount(), 35*5, 
                         "win amount should equal {}.".format(35*5))
    
    def test_lose_amount(self):
        o1 = Outcome("0",35)
        b1 = Bet(5, o1)
        self.assertEqual(b1.lose_amount(), 35*5, 
                         "lose amount should equal {}.".format(35*5))
    
    
if __name__ == "__main__":
    unittest.main()