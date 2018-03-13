import unittest
from roulette import Table, Bet, Outcome
from exceptions import InvalidBet

class TestTable(unittest.TestCase):        
    '''Tests that InvalidBet Exception is thrown when table enters invalid state.
    
    Invalid states are when:
        1. Sum of bets exceeds table limit.
        2. Bet amount is below table minimum.
    '''
    def test_invalid_bet(self):
        table = Table(100,55)
        o1 = Outcome("0", 35)
        b1 = Bet(50, o1)
        b2 = Bet(105, o1)
        b3 = Bet(60, o1)
        self.assertRaises(InvalidBet, table.place_bet, b1)
        self.assertRaises(InvalidBet, table.place_bet, b2)
        
        table2 = Table(100,55)
        table2.place_bet(b3)
        self.assertRaises(InvalidBet, table2.place_bet, b1)
    
    def test_table_add_bet(self):
        '''Tests that bets can be added to the table.'''
        table = Table(100,55)
        o1 = Outcome("0", 35)
        b1 = Bet(60, o1)
        table.place_bet(b1)
        self.assertEqual(b1, next(iter(table)))

if __name__ == "__main__":
    unittest.main()