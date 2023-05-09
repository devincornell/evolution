from __future__ import annotations
import dataclasses
import mase
import typing
import enum
import random
import collections
import json
import copy

#from battlecontroller import BattleController
#import battlecontroller
from .controller import BattleController
from .actions import Action
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
    
class BattleAgentList(typing.List[mase.Agent]):
    def random_order(self, team_id: int = None) -> BattleAgentList:
        '''Get agent ids in a random order.'''
        if team_id is not None:
            agents = [a for a in self if a.state.team_id == team_id]
        else:
            agents = self
        
        return self.__class__(random.sample(agents, len(agents)))
    
    def from_team(self, team_id: int) -> BattleAgentList:
        '''Get agents of a specific team.'''
        return self.__class__(a for a in self if a.state.team_id == team_id)



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
    do_copy_map: bool = False
    verbose: bool = False
    map: mase.HexMap = None
    #pool: mase.AgentPool = dataclasses.field(default_factory=mase.AgentPool)
    #agents: BattleAgentList = dataclasses.field(default_factory=BattleAgentList)
    actions: typing.List[Action] = dataclasses.field(default_factory=list)
    info_history: typing.List[typing.Dict] = dataclasses.field(default_factory=list)
    
    def __post_init__(self):
        '''Each player is a function or callable class to play the game.'''
        self.setup()
        
    def is_finished(self):
        return len(set([a.state.team_id for a in self.map.agents()])) <= 1
        
    def get_winner(self):
        team_id = next(iter(self.map.agents())).state.team_id
        return self.ai_players[team_id]
        
    def step(self):
        for team_id, ai in enumerate(self.ai_players):
            if self.verbose: print(f'Team {team_id} start.')
            if self.do_copy_map:
                # allow users to change only their copied map
                ai_map = copy.deepcopy(self.map)
            else:
                ai_map = self.map
        
            ai_ctrlr = BattleController(team_id, ai_map, verbose=self.verbose)
            ai_agents = BattleAgentList(ai_map.agents())
        
            # execute AI for this turn
            ai(team_id, ai_map, ai_agents, ai_ctrlr)
            
            if self.do_copy_map:
                ctrlr = BattleController(team_id, self.map, verbose=self.verbose)
                ctrlr.apply_actions(ai_ctrlr.get_actions())
                actions = ctrlr.actions()
            else:
                actions = ai_ctrlr.get_actions()
                
            # save info about the game state and actions after each turn
            self.actions.append(actions)
            self.info_history.append(self.get_info())
    
    
    ################### Game Setup ###################
    def setup(self):
        '''Set up actual game.'''
        random.seed(self.map_seed)
        
        self.map = self.generate_random_map()
        #positions = self.map.positions()
        locations = self.map.locations()
        
        # set up agents
        for _ in range(self.num_start_warriors):
            for team_id, player in enumerate(self.ai_players):
                
                # create a new agent and add it to the pool
                agent = mase.Agent(self.next_agent_id(), BattleAgentState(team_id), _map=self.map)
                
                # put agent in free, non-blocked location
                loc = random.choice(locations)
                while loc.state.is_blocked or len(loc.agents):
                    loc = random.choice(locations)
                
                self.map.add_agent(agent, loc.pos)
                
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
        game_map = mase.HexMap(self.map_radius, default_loc_state = BattleLocationState(0, False))
        
        # block off some areas of the map
        all_pos = game_map.positions()
        blocked_pos = random.sample(all_pos, int(len(game_map)*self.blocked_ratio))
        for pos in blocked_pos:
            game_map[pos].state.is_blocked = True
        
        return game_map
        
    def get_info(self):
        return {
            'actions': [[a.get_info() for a in acts] for acts in self.actions],
            'agents': [a.get_info() for a in self.map.agents()],
            'map': self.map.get_info(),
        }
        
    def save_game_state(self, fname: str):
        '''Save the game to disk for replay later.'''
        with open(fname, 'w') as f:
            json.dump(self.info_history, f, indent=2)
        
        
    