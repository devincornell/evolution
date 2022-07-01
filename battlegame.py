import dataclasses
import mase
import typing
import enum
import random
import collections

class BattleAgentState(mase.AgentState):
    id: int
    team: int
    level: int = 1
    speed: int = 1
    
@dataclasses.dataclass
class BattleLocationState:
    food: int
    blocked: bool
    
@dataclasses.dataclass
class BattleController:
    '''This acts like the "Controller" for the game.'''

class BattleGame:
    '''A game implemented using mase.'''
    def __init__(self, map_radius: int, num_start_warriors: int, *ai_players):
        '''Each player is a function or callable class to play the game.
        '''
        self.num_start_warriors = num_start_warriors
        
        self.next_id = 0
        self.pool = mase.AgentStatePool()
        self.map = self.generate_random_map(map_radius)
        self.ai_players = list(enumerate(ai_players))
        
    def next_agent_id(self):
        self.next_id += 1
        return self.next_id - 1
        
    def setup(self):
        '''Set up actual game.'''
        locations = self.map.locations()
        
        for _ in range(self.num_start_warriors):
            for player_id, player in self.ai_players:
                
                # create a new agent and add it to the pool
                agent = BattleAgentState(self.next_agent_id(), player_id)
                self.pool.add(agent.id, agent)
                
                # put agent in free, non-blocked location
                loc = random.choice(locations)
                while not loc['bs'].blocked and not len(loc.agents):
                    loc = random.choice(locations)
                self.map.add_agent(agent.id, loc.pos)
        
    def run(self):
        '''Start the simulation.'''
        while not self.is_finished:
            self.step()
        
    @property
    def is_finished(self):
        return len(collections.Counter([a.team for a in self.pool.values()]))
        
    def step(self):
        pass
    
    @staticmethod
    def generate_random_map(self, map_radius: int) -> mase.HexMap:
        '''Generates a random map according to some conditions.'''
        default_loc_state = {'bs': BattleLocationState(0, False)}
        game_map = mase.HexMap(map_radius, default_loc_state=default_loc_state)
        return game_map
        
