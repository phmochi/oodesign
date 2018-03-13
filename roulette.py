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
        '''Adds straight bets to their bins with odds 35:1.
        
        Each bin (0-36) should have its own straight bet.
        00 should have a similar straight bet at index 37 of the wheel.
        '''
        ODDS = 35
        for n in range(37):
            wheel.add_outcome(n, Outcome("{}".format(n), ODDS))
        wheel.add_outcome(37, Outcome("00", ODDS))
    
    def add_split_bets(self, wheel):
        '''Adds split bets to their corresponding bins with odds 17:1.
        
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
        '''Add street bets to their corresponding bins with odds 11:1.
        
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
        '''Add corner bets to their corresponding bins with odds 8:1.
        
        Corners consist of bins sharing a corner on the board. Between 1-4
        bins can share a corner, but it can be observed that for any corner with
        under 4 bins, a better bet can be made with 4 bins including the original
        bins, so corner bets will only be added for 4 bin sets.
        
        Corners can be found by iterating over the first 2 columns up to the 
        last row and indexing (n, n+1, n+3, n+4). This creates a corner block
        from a bin, its neighbor to the right, its neighbor below it, and its
        neighbor to its bottom right.
        '''
        def add_corner_block(idx, wheel):
            ODDS = 8
            outcome = Outcome("{}-{}-{}-{}".format(*(idx + i for i in [0,1,3,4])), ODDS)
            for i in [0,1,3,4]:
                wheel.add_outcome(idx+i, outcome)
        
        for r in range(11):
            left_n = 3*r + 1
            add_corner_block(left_n, wheel)
            
            right_n = 3*r + 2
            add_corner_block(right_n, wheel)

    def add_line_bets(self, wheel):
        '''Add line bets to their corresponding bins with odds 5:1.
        
        Line blocks consist of 6 bins each. Each line is the line between
        rows on the roulette board. As there are 12 rows, there are 11 lines,
        and relevant bins can be found iterating over consecutive 6 bin blocks
        from the first up to the last row.
        '''
        ODDS = 5
        for r in range(11):
            n = 3*r + 1
            idxs = [n + i for i in range(6)]
            line_outcome = Outcome("{}-{}-{}-{}-{}-{}".format(*idxs), ODDS)
            for idx in idxs:
                wheel.add_outcome(idx, line_outcome)
            
    
    def add_dozen_bets(self, wheel):
        '''Add dozen bets to their corresponding bins with odds 2:1.
        
        Dozen blocks consist of 12 bin intervals: 1-12, 13-24, 25-36.
        '''
        ODDS = 2
        for d in range(3):
            dozen_outcome = Outcome("dozen({})".format(d+1), ODDS)
            for m in range(12):
                idx = 12*d + m + 1
                wheel.add_outcome(idx, dozen_outcome)
    
    def add_column_bets(self, wheel):
        '''Add column bets to their corresponding bins with odds 2:1.
        
        Column blocks consist of the 12 bins in a single column.
        '''
        ODDS = 2
        for c in range(3):
            col_outcome = Outcome("column({})".format(c+1), ODDS)
            for r in range(12):
                idx = 3*r + c + 1
                wheel.add_outcome(idx, col_outcome)
    
    def add_even_money_bets(self, wheel):
        '''Add even money bets to their corresponding bins with odds 1:1.
        
        Even money bets consist of 6 types:
            1. Red
                Red bins on the boards.
            2. Black
                Black bins on the board.
            3. Even
                Even bins on the board.
            4. Odd
                Odd bins on the board.
            5. High
                Bins < 19.
            6. Low
                Bins >= 19.
        '''
        ODDS = 1
        red = Outcome("red", ODDS)
        black = Outcome("black", ODDS)
        even = Outcome("even", ODDS)
        odd = Outcome("odd", ODDS)
        high = Outcome("high", ODDS)
        low = Outcome("low", ODDS)
        
        red_bins = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
        
        for n in range(1, 37):
            if n >= 1 and n < 19:
                wheel.add_outcome(n, low)
            else:
                wheel.add_outcome(n, high)
                
            if n % 2 == 0:
                wheel.add_outcome(n, even)
            else:
                wheel.add_outcome(n, odd)
                
            if n in red_bins:
                wheel.add_outcome(n, red)
            else:
                wheel.add_outcome(n, black)
        
    def build_bins(self, wheel):
        self.add_straight_bets(wheel)
        self.add_split_bets(wheel)
        self.add_street_bets(wheel)
        self.add_corner_bets(wheel)
        self.add_line_bets(wheel)
        self.add_dozen_bets(wheel)
        self.add_column_bets(wheel)
        self.add_even_money_bets(wheel)
    