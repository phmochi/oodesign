from roulette import Bin, Outcome

class TestBin:    
    def setup_method(self):
        self.o1 = Outcome("0", 35)
        self.o2 = Outcome("00", 35)
        
    def test_add_outcomes(self):
        '''Checks that Bin can accept a list of Outcome'''
        b1 = Bin([self.o1,self.o2])
        assert self.o1 in b1
        assert self.o2 in b1
        
    def test_multiple_references(self):
        '''Checks that Outcome can be in multiple Bins'''
        b1 = Bin([self.o1])
        b2 = Bin([self.o1])
        assert self.o1 in b1
        assert self.o1 in b2
        
    def test_outcome_iterator(self):
        b1 = Bin([self.o1, self.o2])
        iterator = b1.get_outcome_iterator()
        assert next(iterator) in [self.o1, self.o2]
        assert next(iterator) in [self.o1, self.o2]