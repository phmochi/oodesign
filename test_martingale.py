from roulette import Martingale, Table, Wheel

def test_martingale_bet():
    '''Test Martingale's bets update correctly.'''
    w = Wheel(1)
    t = Table(100,1,w)
    m = Martingale(t)
    
    lose_streak = 0
    simulation = Wheel(1)
    m.place_bets()
    for _ in range(5):
        m.place_bets()
        
        assert t.bets[0].amount == 2**lose_streak
        
        won = simulation.get_outcome("black") in simulation.next()
        if won:
            lose_streak = 0
            m.win(t.bets[0])
        else:
            lose_streak += 1
            m.lose(t.bets[0])
        t.clear_bets()