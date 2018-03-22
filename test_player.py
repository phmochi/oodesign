from roulette import Wheel, SimulationBuilder
import random

class TestPlayer:
    '''Checks that various Player classes bet as their strategy recommends'''
    def setup_method(self):
        self.sb = SimulationBuilder(table_limit=1000, seed=1)
        
    def test_martingale_bet(self):
        '''Test Martingale's bets update correctly.'''
        simulator = self.sb.get_simulator("martingale")
        m = simulator.player
        
        lose_streak = 0
        simulation = Wheel(1)
        
        m.set_stake(100)
        m.set_rounds(5)
        
        for _ in range(5):
            m.place_bets()
            
            assert m.table.bets[0].amount == 2**lose_streak
            
            won = simulation.get_outcome("black") in simulation.next()
            if won:
                lose_streak = 0
                m.win(m.table.bets[0])
            else:
                lose_streak += 1
                m.lose(m.table.bets[0])
            m.table.clear_bets()
        
    def test_field_ops(self):
        '''Checks that the simulator can correctly set Players' rounds and stakes'''
        simulator = self.sb.get_simulator("martingale")
        m = simulator.player
        
        assert m.stake == None
        assert m.rounds == None
        
        m.set_stake(10)
        m.set_rounds(20)
        
        assert m.stake == 10
        assert m.rounds == 20
        
    def test_sevenreds_bet(self):
        '''Check that SevenReds bets after there are 7 consecutive reds.'''
        simulation = Wheel(1)
        
        simulator = self.sb.get_simulator("sevenreds")
        game = simulator.game
        simulator.player.set_rounds(simulator.init_duration)
        simulator.player.set_stake(simulator.init_stake)
        
        red_streak = 0
        red = simulation.get_outcome("red")
        for _ in range(simulator.player.rounds):
            _, num_bets = game.cycle(simulator.player) 
            assert (red_streak >= 7) == bool(num_bets)
            
            winners = simulation.next()
            if red in winners:
                red_streak += 1
            else:
                red_streak = 0
    
    def test_sevenreds_counter(self):
        '''Checks that SevenReds red counter increments correctly.'''
        simulation = Wheel(1)
        
        simulator = self.sb.get_simulator("sevenreds")
        game = simulator.game
        
        red_streak = 0
        red = simulation.get_outcome("red")
        for _ in range(10):
            winners = simulation.next()
            if red in winners:
                red_streak += 1
            else:
                red_streak = 0
                
            game.cycle(simulator.player)
            assert simulator.player.red_count == red_streak
            
    def test_player_random(self):
        '''Checks that PlayerRandom bets the same as pseudorandom.'''
        simulator = self.sb.get_simulator("random")
        simulator.player.set_rounds(simulator.init_duration)
        simulator.player.set_stake(simulator.init_stake)
        
        all_outcomes = simulator.game.table.wheel.get_all_outcomes()
        
        r = random.Random(1)
        for _ in range(5):
            assert r.sample(all_outcomes, 1)[0] == simulator.player.place_bets().outcome