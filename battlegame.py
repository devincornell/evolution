import dataclasses
import mase
import typing
import enum
import random
import collections
import json
import copy

#from battlecontroller import BattleController
import battlecontroller
from mase.agent import Agent

@dataclasses.dataclass
class BattleAgentState(mase.AgentState):
    team_id: int
    level: int = 1
    health: int = 1
    
    def get_info(self):
        return dataclasses.asdict(self)
    
    @property
    def speed(self):
        '''Number of steps an agent can take in oen turn.'''
        return 1
    
    @property
    def attack(self):
        '''Health removed from other agent after attacking.'''
        return self.level
    
    @property
    def max_health(self):
        return self.level
    
@dataclasses.dataclass
class BattleLocationState(mase.LocationState):
    num_orbs: int
    is_blocked: bool
    def get_info(self):
        return {'num_orbs': self.num_orbs, 'is_blocked': self.is_blocked}

@dataclasses.dataclass
class BattleGame:
    '''A game implemented using mase.'''
    ai_players: typing.List[typing.Callable]
    map_radius: int
    blocked_ratio: float
    orb_ratio: float
    num_start_warriors: int
    map_seed: int = 0
    max_turns: int = 100
    next_id: int = 0
    map: mase.HexNetMap = None
    #pool: mase.AgentPool = dataclasses.field(default_factory=mase.AgentPool)
    agents: typing.List[Agent] = dataclasses.field(default_factory=list)
    actions: typing.List[battlecontroller.Action] = dataclasses.field(default_factory=list)
    info_history: typing.List[typing.Dict] = dataclasses.field(default_factory=list)
    
    def __post_init__(self):
        '''Each player is a function or callable class to play the game.'''
        self.setup()
        
    def run(self):
        '''Start the simulation.'''
        i = 1
        while not self.is_finished():
            self.step()
            i += 1
            
            if i > self.max_turns:
                break
        
    def is_finished(self):
        return len(set([a.state.team_id for a in self.map.agents])) <= 1
        
    def get_winner(self):
        team_id = next(iter(self.map.agents)).state.team_id
        return self.ai_players[team_id]
        
    def step(self):
        for team_id, ai in enumerate(self.ai_players):
            
            # prepare interface for AI to use
            #new_map = self.map.deepcopy()
            #new_pool = self.pool.deepcopy()
            #ai_controller = battlecontroller.BattleController(team_id, new_map, new_pool)
            ctrlr = battlecontroller.BattleController(team_id, self.map)
            
            # execute AI for this turn
            #ai(team_id, new_map, new_pool, ctrlr)
            ai(team_id, self.map, self.map.agents, ctrlr)
            
            # get user actions and apply them to real map and pool
            #game_controller = battlecontroller.BattleController(team_id, self.map, self.pool)
            #game_controller.apply_actions(ai_controller.get_actions())
            self.actions.append(ctrlr.get_actions())
            
            # save info about the game state after each turn
            self.info_history.append(self.get_info())
            #print(self.get_info()['agents'])
    
    
    ################### Game Setup ###################
    def setup(self):
        '''Set up actual game.'''
        random.seed(self.map_seed)
        
        self.map = self.generate_random_map()
        positions = self.map.positions()
        
        # set up agents
        for _ in range(self.num_start_warriors):
            for team_id, player in enumerate(self.ai_players):
                
                # create a new agent and add it to the pool
                agent = mase.Agent(self.next_agent_id(), BattleAgentState(team_id), _map=self.map)
                
                # put agent in free, non-blocked location
                loc = random.choice()
                while loc.state.is_blocked or len(loc.agents):
                    pos = random.choice(positions)
                    self.map.add_agent(agent, pos)
                
        # spread orbs
        free_loc = set([loc for loc in self.map.locations() if not loc.state.is_blocked])
        for loc in random.sample(free_loc, int(len(free_loc)*self.orb_ratio)):
            loc.state.num_orbs += 1
        
        # add initial game state to history
        self.info_history.append(self.get_info())
    
    def next_agent_id(self):
        self.next_id += 1
        return self.next_id - 1
    
    def generate_random_map(self) -> mase.HexMap:
        '''Generates a random map according to some conditions.'''
        game_map = mase.HexMap(self.map_radius, default_state = BattleLocationState(0, False))
        
        # block off some areas of the map
        blocked_pos = random.sample(game_map.positions, int(len(game_map)*self.blocked_ratio))
        for pos in blocked_pos:
            game_map[pos].state.is_blocked = True
        
        return game_map
        
    def get_info(self):
        return {
            'actions': [[a.get_info() for a in tactions] for tactions in self.actions],
            'agents': [a.get_info() for a in self.map.agents],
            'map': self.map.get_info(),
        }
        
    def save_game_state(self, fname: str):
        '''Save the game to disk for replay later.'''
        with open(fname, 'w') as f:
            json.dump(self.info_history, f, indent=2)
        
        
    