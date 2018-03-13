import unittest
import random
from roulette import Outcome, Bin, Wheel

class GIVEN_wheel_WHEN_next_THEN_random_choice(unittest.TestCase):
    def setUp(self):
        self.wheel = Wheel(1)
    
    def test_add_bin(self):
        b1 = Bin([Outcome("0", 35)])
        self.wheel.add_bin(10, b1)
        self.assertEqual(self.wheel.get(10), b1, "Added bin doesn't match.")
        
    def test_next(self):
        r = random.Random()
        r.setstate(self.wheel.rng.getstate())
        
        b1 = Bin([Outcome("Red", 5)])
        b2 = Bin([Outcome("0", 35), Outcome("Black", 5)])
        
        self.wheel.add_bin(r.randint(0,38), b1)
        self.wheel.add_bin(r.randint(0,38), b2)
        
        self.assertEqual(self.wheel.next(), b1, "Next doesn't return correct bin.")
        self.assertEqual(self.wheel.next(), b2, "Next doesn't return correct bin.")
        self.assertNotEqual(self.wheel.next(), b2, "Next should not return same bin.")
        
    def test_add_outcome(self):
        o1 = Outcome("0",35)
        o2 = Outcome("00", 35)
        
        b1 = Bin([o1])
        b2 = Bin([o1,o2])
        
        self.wheel.add_outcome(4, o1)
        self.assertEqual(self.wheel.get(4), b1, "Bin not equivalent after adding Outcome.")
        self.wheel.add_outcome(4, o2)
        self.assertEqual(self.wheel.get(4), b2, "Bin not equivalent after adding Outcome.")
        
    def test_get_bin(self):
        b1 = Bin([Outcome("Red", 5)])
        self.wheel.add_bin(3, b1)
        self.assertEqual(self.wheel.get(3), b1, "Retrieved bin not correct.")
    
if __name__ == "__main__":
    unittest.main()