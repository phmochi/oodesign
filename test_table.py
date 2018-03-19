import pytest
from roulette import Table, Bet, Outcome, Wheel
from exceptions import InvalidBet

class TestTable:
    '''Tests that InvalidBet Exception is thrown when table enters invalid state.
    
    Invalid states are when:
        1. Sum of bets exceeds table limit.
        2. Bet amount is below table minimum.
    '''
    def setup_method(self, method):
        wheel = Wheel()
        self.table = Table(100, wheel)
    
    def test_invalid_bet(self):
            
        with pytest.raises(InvalidBet):
            self.table.place_bet(Bet(105, Outcome("0",35)))
            
        table2 = Table(100, self.table.wheel)
        table2.place_bet(Bet(60, Outcome("0",35)))
        with pytest.raises(InvalidBet):
            self.table.place_bet(Bet(50, Outcome("0",35)))
            
    def test_add_bet(self):
        bet = Bet(60, Outcome("0",35))
        self.table.place_bet(bet)
        assert bet == next(iter(self.table)) 
        
    def test_table_clear_bet(self):
        self.table.place_bet(Bet(60, Outcome("0",35)))
        assert len(self.table.bets) == 1
        
        self.table.clear_bets()
        assert len(self.table.bets) == 0
        
    