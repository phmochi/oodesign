from roulette import Simulator, Martingale, Game, Wheel, Table

class TestSimulator():
    '''Checks that Simulator's results match a seeded simulation results.'''
    def setup_method(self):
        wheel = Wheel(1)
        table = Table(100,1,wheel)
        martingale = Martingale(table)
        game = Game(table)
        
        assert martingale.rounds == None
        assert martingale.stake == None
        
        self.simulator = Simulator(game, martingale)
        
    def test_simulator_session(self):
        simulation_wheel = Wheel(1)
        simulation_table = Table(100,1,simulation_wheel)
        simulation_player = Martingale(simulation_table)
        simulation_player.set_rounds(self.simulator.init_duration)
        simulation_player.set_stake(self.simulator.init_stake)
        black = simulation_player.black #Martingale always bets on black
        
        simulated_stakes = [simulation_player.stake]
        while simulation_player.playing():
            simulation_player.place_bets()
            outcome = simulation_wheel.next() 
            
            if black in outcome:
                simulation_player.win(simulation_table.bets[0])
            else:
                simulation_player.lose(simulation_table.bets[0])
                
            simulation_table.clear_bets()
            simulated_stakes.append(simulation_player.stake)
    
        stakes = self.simulator.session()
        
        assert type(stakes) == list
        assert stakes == simulated_stakes
        
    def test_simulator_gather(self):
        self.simulator.gather()
        
        assert len(self.simulator.durations) == self.simulator.samples
        assert len(self.simulator.maxima) == self.simulator.samples