from roulette import Game, Passenger57, Table, Wheel

class TestGame:    
    def setup_method(self):
        self.random_seed = 1
        w = Wheel(seed=self.random_seed)
        self.t = Table(100,5, w)
        self.p = Passenger57(self.t)
        self.g = Game(table=self.t)    
    
    def test_game_initialization(self):
        '''Checks that game initializes with a wheel and a table'''
        assert isinstance(self.g.table.wheel, Wheel)
        assert isinstance(self.g.table, Table)
    
    def test_passenger57(self):
        '''Checks that player bets are added to Table'''
        self.p.place_bets()
        assert self.p.black in [x.outcome for x in self.t.bets]
    
    def test_game_cycle(self):
        '''Simulates a few game cycles to check that the correct number of 
        winning bets are returned.
        '''
        simulator = Wheel(seed=self.random_seed)
        outcomes = [simulator.next()]
        outcomes.append(simulator.next())
        outcomes.append(simulator.next())
        
        for o in outcomes:
            if self.p.black in o:
                assert self.g.cycle(self.p) > 0
            else:
                assert self.g.cycle(self.p) == 0
            