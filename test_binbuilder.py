import unittest
from roulette import Wheel, Outcome, BinBuilder

class TestBinBuilder(unittest.TestCase):
    def setUp(self):
        self.wheel = Wheel()
        bb = BinBuilder()
        bb.build_bins(self.wheel)
        
    def test_straight_bets(self):
        '''
        Each bin (0-36) should have its own straight bet with odds 35:1.
        00 should have a similar straight bet at index 37 of the wheel.
        '''
        for i in range(0,37):
            self.assertIn(Outcome("{}".format(i), 35), self.wheel.get(i), "{} not in bin.".format(i))
        self.assertIn(Outcome("00", 35), self.wheel.get(37), "00 not in bin.")
        
    def test_split_bets(self):
        '''
        A pair consists of two adjacent bins, left/right or top/down.
        Left/right pairs can be found by iterating over the first 2 columns,
        and finding the corresponding bin to the right (n, n+1).
        Top/down pairs can be found by iterating over every element not in the
        last row and finding the corresponding bin below it (n, n+3).
        '''
        def check_offset(self, n, offset):
            '''
            Checks that an outcome is in a bin with index, n, and its offset,
            n + offset.
            '''
            m = "Split bet not in bin."
            split_bet = Outcome("{}-{}".format(n,n+offset), 17)
            self.assertIn(split_bet, self.wheel.get(n), m)
            self.assertIn(split_bet, self.wheel.get(n+offset), m)
        
        def test_left_right_pairs(self):
            '''Checks bin with index, n, and the bin to its right, n+1.'''
            for row in range(12):
                for i in range(1,3):
                    n = 3*row + i
                    check_offset(self, n, 1)
        
        def test_top_down_pairs(self):
            '''Checks bin with index, n, and the bin below it, n+3.'''
            for row in range(11):
                for i in range(1,4):
                    n = 3*row + i
                    check_offset(self, n, 3)
        
        test_left_right_pairs(self)
        test_top_down_pairs(self)
        
    def test_street_bets(self):
        '''
        A street bet consists of a row of 3 bins.
        Street bets can be found by iterating over each element in the first
        column and finding its neighbors, (n, n+1, n+2).
        '''
        for row in range(12):
            n = 3*row + 1
            street_bet = Outcome("{}-{}-{}".format(n,n+1,n+2), 11)
            self.assertIn(street_bet, self.wheel.get(n))
            self.assertIn(street_bet, self.wheel.get(n+1))
            self.assertIn(street_bet, self.wheel.get(n+2))
            
    def test_corner_bets(self):
        '''
        Corners consist of bins sharing a corner on the board. Between 1-4
        bins can share a corner, but it can be observed that for any corner with
        under 4 bins, a better bet can be made with 4 bins including the original
        bins, so corner bets will only be added for 4 bin sets.
        
        Corners can be found by iterating over the first 2 columns up to the 
        last row and indexing (n, n+1, n+3, n+4). This creates a corner block
        from a bin, its neighbor to the right, its neighbor below it, and its
        neighbor to its bottom right.
        '''
        def check_corner(self, n)    :
            corner_bet = Outcome("{}-{}-{}-{}".format(n,n+1,n+3,n+4), 8)
            self.assertIn(corner_bet, self.wheel.get(n))
            self.assertIn(corner_bet, self.wheel.get(n+1))
            self.assertIn(corner_bet, self.wheel.get(n+3))
            self.assertIn(corner_bet, self.wheel.get(n+4))
    
        for row in range(11):
            n = 3*row + 1
            check_corner(self, n)
            
            n2 = 3*row + 2
            check_corner(self, n2)
    
    def test_line_bets(self):
        '''
        Line blocks consist of 6 bins each. Each line is the line between
        rows on the roulette board. As there are 12 rows, there are 11 lines,
        and relevant bins can be found iterating over consecutive 6 bin blocks
        from the first up to the last row.
        '''
        for row in range(10):
            n = 3*row + 1
            line_bet = Outcome("{}-{}-{}-{}-{}-{}".format(*(n+i for i in 
                               range(6))), 5)
            for i in range(6):
                self.assertIn(line_bet, self.wheel.get(n+i))
    
    def test_dozen_bets(self):
        '''Dozen blocks consist of 12 bin intervals: 1-12, 13-24, 25-36.'''
        for d in range(3):
            dozen_bet = Outcome("dozen({})".format(d+1), 2)
            for m in range(12):
                idx = 12*d + m + 1
                self.assertIn(dozen_bet, self.wheel.get(idx))
    
    def test_column_bets(self):
        '''Column blocks consist of the 12 bins in a single column.'''
        for c in range(3):
            column_bet = Outcome("column({})".format(c+1), 2)
            for r in range(12):
                idx = 3*r + c + 1
                self.assertIn(column_bet, self.wheel.get(idx))
    
    def test_even_money_bets(self):
        '''
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
        red = Outcome("red", 1)
        black = Outcome("black", 1)
        even = Outcome("even", 1)
        odd = Outcome("odd", 1)
        high = Outcome("high", 1)
        low = Outcome("low", 1)
        
        red_bins = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
        for n in range(1,37):
            if n >= 1 and n < 19:
                self.assertIn(low, self.wheel.get(n))
            elif n >= 19 and n < 37:
                self.assertIn(high, self.wheel.get(n))
                
            if n % 2 == 0:
                self.assertIn(even, self.wheel.get(n))
            else:
                self.assertIn(odd, self.wheel.get(n))
            
            if n in red_bins:
                self.assertIn(red, self.wheel.get(n))
            else:
                self.assertIn(black, self.wheel.get(n))
                
    def test_five_bets(self):
        '''Bins for 0 and 00 contain "Five Bet" Outcome (00-0-1-2-3)'''
        five_bet_outcome = Outcome("00-0-1-2-3", 6)
        self.assertIn(five_bet_outcome, self.wheel.get(0))
        self.assertIn(five_bet_outcome, self.wheel.get(37))
                
    def test_bin_lens(self):
        ans = [2,12,14,12,14,17,14,14,17,14,14,17,14,14,17,14,14,17,14,14,17, \
               14,14,17,14,14,17,14,14,17,14,14,17,14,11,13,11,2]
        
        self.assertListEqual(ans, [len(x) for x in self.wheel.bins],
                                   "Bin lengths do not match.")
        
if __name__ == "__main__":
    unittest.main()