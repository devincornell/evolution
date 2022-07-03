import dataclasses
import mase
import typing
import enum
import random
import collections

from .battlecontroller import BattleController
#import battlecontroller

@dataclasses.dataclass
class BattleAgentState(mase.AgentState):
    id: int
    team_id: int
    level: int = 1
    health: int = 1
    
    @property
    def speed(self):
        '''Number of steps an agent can take in oen turn.'''
        return self.level
    
    @property
    def attack(self):
        '''Health removed from other agent after attacking.'''
        return self.level
    
    @property
    def max_health(self):
        return self.level
    
@dataclasses.dataclass
class BattleLocationState(mase.LocationState):
    orbs: int
    is_blocked: bool
    

class BattleGame:
    '''A game implemented using mase.'''
    def __init__(self, ai_players: typing.List[typing.Callable], map_radius: int, blocked_ratio: float, food_ratio: float, num_start_warriors: int):
        '''Each player is a function or callable class to play the game.
        '''
        self.num_start_warriors = num_start_warriors
        self.food_ratio = food_ratio
        self.ai_players = list(ai_players)
        
        self.next_id: int = 0
        self.pool: mase.AgentStatePool = mase.AgentStatePool()
        self.map: mase.HexMap = self.generate_random_map(map_radius, blocked_ratio)
        self.controller = BattleController()
        
        
    def run(self):
        '''Start the simulation.'''
        while not self.is_finished:
            self.step()
        
    @property
    def is_finished(self):
        return len(set([a.team for a in self.pool.values()])) <= 1
        
    def step(self):
        for team_id, ai in enumerate(self.ai_players):
            new_map = self.map.deepcopy()
            new_pool = self.pool.deepcopy()
            ai_controller = BattleController(team_id, new_map, new_pool)
            
            # actually execute ai
            ai(team_id, new_map, new_pool, ai_controller)
            
            # get user actions and apply them to real map and pool
            game_controller = BattleController(team_id, self.map, self.pool)
            game_controller.apply_actions(ai_controller.get_actions())
            
            
    
    ################### Game Setup ###################
    def setup(self):
        '''Set up actual game.'''
        locations = self.map.locations()
        
        # set up agents
        for _ in range(self.num_start_warriors):
            for player_id, player in enumerate(self.ai_players):
                
                # create a new agent and add it to the pool
                agent = BattleAgentState(self.next_agent_id(), player_id)
                self.pool.add(agent.id, agent)
                
                # put agent in free, non-blocked location
                loc = random.choice(locations)
                while not loc.state.is_blocked and not len(loc.agents):
                    loc = random.choice(locations)
                self.map.add_agent(agent.id, loc.pos)
                
        # spread orbs
        free_loc = set([loc for loc in self.map.locations if not loc.state.is_blocked])
        for loc in random.choices(free_loc, int(len(free_loc)*self.food_ratio)):
            loc.state.orbs
    
    def next_agent_id(self):
        self.next_id += 1
        return self.next_id - 1
    
    @staticmethod
    def generate_random_map(self, map_radius: int, blocked_ratio: float) -> mase.HexMap:
        '''Generates a random map according to some conditions.'''
        game_map = mase.HexMap(map_radius, default_state = BattleLocationState)
        
        # block off some areas of the map
        blocked_pos = random.choices(game_map.positions, int(len(game_map)*blocked_ratio))
        for pos in blocked_pos:
            game_map[pos].state.is_blocked = True
        
        return game_map
        
if __name__ == '__main__':
    def example_ai(team_id: int, game_map: mase.HexMap, agents: mase.AgentStatePool):
        print(f'Starting team {team_id} turn!')
    
    game = BattleGame()