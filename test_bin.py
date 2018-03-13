import unittest
from roulette import Bin, Outcome

class TestBin(unittest.TestCase):
    
    def test_add_outcomes(self):
        '''Checks that Bin can accept a list of Outcome'''
        o1 = Outcome("0", 35)
        o2 = Outcome("00", 35)
        b1 = Bin([o1,o2])
        self.assertIn(o1, b1, "outcome not added to bin.")
        self.assertIn(o2, b1, "outcome not added to bin.")
        
    def test_multiple_references(self):
        '''Checks that Outcome can be in multiple Bins'''
        o1 = Outcome("0", 35)
        b1 = Bin([o1])
        b2 = Bin([o1])
        self.assertIn(o1, b1, "outcome not shared in bin.")
        self.assertIn(o1, b2, "outcome not shared in bin.")    
        
if __name__ == "__main__":
    unittest.main()