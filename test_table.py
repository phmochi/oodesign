import unittest
from roulette import Table, Bet, Outcome
from exceptions import InvalidBet

class TestTable(unittest.TestCase):        
    '''Tests that InvalidBet Exception is thrown when table enters invalid state.
    
    Invalid states are when:
        1. Sum of bets exceeds table limit.
        2. Bet amount is below table minimum.
    '''
    def setUp(self):
        self.table1 = Table(100,55)
        self.table2 = Table(100,55)
        self.o1 = Outcome("0", 35)
        self.b1 = Bet(50, self.o1)
        self.b2 = Bet(105, self.o1)
        self.b3 = Bet(60, self.o1)
        
    def test_invalid_bet(self):
        self.assertRaises(InvalidBet, self.table1.place_bet, self.b1)
        self.assertRaises(InvalidBet, self.table1.place_bet, self.b2)
        
        self.table2.place_bet(self.b3)
        self.assertRaises(InvalidBet, self.table2.place_bet, self.b1)
    
    def test_table_add_bet(self):
        '''Tests that bets can be added to the table.'''
        self.table1.place_bet(self.b3)
        self.assertEqual(self.b3, next(iter(self.table1)))
        
    def test_table_clear_bet(self):
        self.table1.place_bet(self.b3)
        self.assertEqual(len(self.table1.bets), 1)
        
        self.table1.clear_bets()
        self.assertEqual(len(self.table1.bets), 0)

if __name__ == "__main__":
    unittest.main()