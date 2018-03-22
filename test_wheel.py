import random
from roulette import Outcome, Bin, Wheel

class TestWheel:
    def setup_method(self):
        self.wheel = Wheel(1)
        
    def test_initialize(self):
        assert len(self.wheel.bins) == 38
        for b in self.wheel.bins:
            assert len(b) > 0
            assert len(b) < 20
    
    def test_add_bin(self):
        b1 = Bin([Outcome("0", 35)])
        self.wheel.add_bin(10, b1)
        assert self.wheel.get(10) == b1
        
    def test_next(self):
        r = random.Random()
        r.setstate(self.wheel.rng.getstate())
        
        b1 = Bin([Outcome("Red", 5)])
        b2 = Bin([Outcome("0", 35), Outcome("Black", 5)])
        
        self.wheel.add_bin(r.randint(0,38), b1)
        self.wheel.add_bin(r.randint(0,38), b2)
        
        assert self.wheel.next() == b1
        assert self.wheel.next() == b2
        assert self.wheel.next() != b2
        
    def test_add_outcome(self):
        o1 = Outcome("test",35)
        
        self.wheel.add_outcome(4, o1)
        assert o1 in self.wheel.get(4)
        
    def test_get_bin(self):
        b1 = Bin([Outcome("Red", 5)])
        self.wheel.add_bin(3, b1)
        assert self.wheel.get(3) == b1
        
    def test_get_outcome(self):
        o1 = Outcome("0", 35)
        self.wheel.add_outcome(4, o1)
        
        assert self.wheel.get_outcome("0") == o1
        assert self.wheel.get_outcome("gibberish") == None
        
    def test_get_bin_iterator(self):
        iterator = self.wheel.get_all_bins()
        for i in range(37):
            bin_iter = next(iterator)
            assert isinstance(bin_iter, Bin) == True
            assert self.wheel.get_outcome("{}".format(i)) in bin_iter.get_outcome_iterator()
        
        assert self.wheel.get_outcome("00") in next(iterator)