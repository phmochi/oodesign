import random

class Outcome:
    def __init__(self, name, odds):
        '''Represents an Outcome, for handling bets
        
        Parameters:
            name: str
            odds: number
        
        '''
        self.name = name
        self.odds = odds
        
    def win_amount(self, amount):
        '''Calculates the total win amount.
        
        Parameters:
            amount : number
        
        Returns:
            number : amount * odds
        '''
        return amount*self.odds
    
    def __eq__(self, other):
        '''Return True if both Outcomes have the same name'''
        return self.name == other.name
    
    def __ne__(self, other):
        '''Return True if both Outcomes do not have the same name'''
        return ~(self.name == other.name)
    
    def __hash__(self):
        '''Returns hash value of name property (string)'''
        return hash(self.name)
    
    def __str__(self):
        return "{} (odds:{})".format(self.name, self.odds)
    
    def __repr__(self):
        return "Outcome({}, {})".format(self.name, self.odds)
    
class Bin(frozenset): 
    '''Represents the 38 bins of the roulette wheel.
    
    Contains a collection of winning Outcomes for the corresponding bin.
    '''
    pass

class Wheel:
    '''Manages and randomly selects a bin to simulate a roulette wheel.
    
    Fields:
        bins: Contains bin instances.
        rng: Random number generator used to select bins.
    '''
    
    def __init__(self, seed=None):
        self.bins = [Bin([]) for _ in range(38)]
        self.rng = random.Random()
        if seed:
            self.rng.seed(seed)
        
    def add_outcome(self, number, outcome):
        self.bins[number] |= Bin([outcome])
    
    def add_bin(self, idx, bin):
        self.bins[idx] = bin
    
    def next(self):
        return self.bins[self.rng.randint(0,38)]
    
    def get(self, idx):
        return self.bins[idx]
    
class BinBuilder:
    def add_straight_bets(self, wheel):
        '''Adds straight bets to their bins with odds 1:35.
        
        Each bin (0-36) should have its own straight bet.
        00 should have a similar straight bet at index 37 of the wheel.
        '''
        ODDS = 35
        for n in range(37):
            wheel.add_outcome(n, Outcome("{}".format(n), ODDS))
        wheel.add_outcome(37, Outcome("00", ODDS))
    
    def add_split_bets(self, wheel):
        '''Adds split bets to their corresponding bins with odds 1:17.
        
        A pair consists of two adjacent bins, left/right or top/down.
        Left/right pairs can be found by iterating over the first 2 columns,
        and finding the corresponding bin to the right (n, n+1).
        Top/down pairs can be found by iterating over every element not in the
        last row and finding the corresponding bin below it (n, n+3).
        '''
        def add_left_right_pair(outcome, idx, wheel):
            wheel.add_outcome(idx, outcome)
            wheel.add_outcome(idx+1, outcome)
            
        def add_top_down_pair(outcome, idx, wheel):
            wheel.add_outcome(idx, outcome)
            wheel.add_outcome(idx+3, outcome)
        
        ODDS = 17
        for r in range(12):
            for i in range(1,3):
                n = 3*r + i
                pair_outcome = Outcome("{}-{}".format(n, n+1), ODDS)
                add_left_right_pair(pair_outcome, n, wheel)
                
        for n in range(1,34):
            pair_outcome = Outcome("{}-{}".format(n, n+3), ODDS)
            add_top_down_pair(pair_outcome, n, wheel)
    
    def add_street_bets(self, wheel):
        '''Add street bets to their corresponding bins with odds 1:11.
        
        A street bet consists of a row of 3 bins.
        Street bets can be found by iterating over each element in the first
        column and finding its neighbors, (n, n+1, n+2).
        '''
        ODDS = 11
        for r in range(12):
            n = 3*r+1
            street_outcome = Outcome("{}-{}-{}".format(n,n+1,n+2), ODDS)
            for i in range(3):
                wheel.add_outcome(n+i, street_outcome)
    
    def add_corner_bets(self, wheel):
        pass

    def add_line_bets(self, wheel):
        pass
    
    def add_dozen_bets(self, wheel):
        pass
    
    def add_column_bets(self, wheel):
        pass
    
    def add_even_money_bets(self, wheel):
        pass
        
    def build_bins(self, wheel):
        self.add_straight_bets(wheel)
        self.add_split_bets(wheel)
        self.add_street_bets(wheel)
        self.add_corner_bets(wheel)
        self.add_line_bets(wheel)
        self.add_dozen_bets(wheel)
        self.add_column_bets(wheel)
        self.add_even_money_bets(wheel)
    