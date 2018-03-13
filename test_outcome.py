import unittest
from roulette import Outcome

class TestOutcome(unittest.TestCase):
    
    def test_eq(self):
        '''Check that same Outcomes are equal'''
        o1 = Outcome("Any Craps", 8)
        o2 = Outcome("Any Craps", 8)
        self.assertEqual(o1, o2, "Outcomes not equal.")
        
    def test_neq(self):
        '''Check that different Outcomes are not equal'''
        o1 = Outcome("Any Craps", 8)
        o2 = Outcome("Red", 1)
        self.assertNotEqual(o1, o2, "Outcomes should not be equal.")
        
    def test_hash(self):
        '''Check that same Outcomes have the same hash'''
        o1 = Outcome("Any Craps", 8)
        o2 = Outcome("Any Craps", 8)
        self.assertEqual(hash(o1), hash(o2), "Hashes not equal.")
        
    def test_win_amount(self):
        '''Check that win amounts are calculated correctly'''
        o1 = Outcome("Any Craps", 8)
        self.assertEqual(40, o1.win_amount(5), "Win amount doesn't match.")
        
if __name__ == "__main__":
    unittest.main()