import dataclasses
import mase
import typing
import enum
import random
import collections
import json

#from battlecontroller import BattleController
import battlecontroller

@dataclasses.dataclass
class BattleAgentState(mase.AgentState):
    id: mase.AgentID
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
    orbs: int
    is_blocked: bool
    def get_info(self):
        return {'orbs': self.orbs, 'is_blocked': self.is_blocked}

@dataclasses.dataclass
class BattleGame:
    '''A game implemented using mase.'''
    ai_players: typing.List[typing.Callable]
    map_radius: int
    blocked_ratio: float
    food_ratio: float
    num_start_warriors: int
    map_seed: int = 0
    max_turns: int = 100
    next_id: int = 0
    map: mase.HexMap = None
    pool: mase.AgentPool = dataclasses.field(default_factory=mase.AgentPool)
    actions: typing.List[battlecontroller.Action] = dataclasses.field(default_factory=list)
    info_history: typing.List[typing.Dict] = dataclasses.field(default_factory=list)
    
    def __post_init__(self):
        '''Each player is a function or callable class to play the game.'''
        self.setup()
        
    def run(self):
        '''Start the simulation.'''
        i = 1
        while not self.is_finished:
            print(f'Starting turn {i}.')
            self.step()
            i += 1
            
            if i > self.max_turns:
                break
        
    @property
    def is_finished(self):
        return len(set([a.state.team_id for a in self.pool])) <= 1
        
    def step(self):
        for team_id, ai in enumerate(self.ai_players):
            
            # prepare interface for AI to use
            #new_map = self.map.deepcopy()
            #new_pool = self.pool.deepcopy()
            #ai_controller = battlecontroller.BattleController(team_id, new_map, new_pool)
            ctrlr = battlecontroller.BattleController(team_id, self.map, self.pool)
            
            # execute AI for this turn
            #ai(team_id, new_map, new_pool, ctrlr)
            ai(team_id, self.map, self.pool, ctrlr)
            
            # get user actions and apply them to real map and pool
            #game_controller = battlecontroller.BattleController(team_id, self.map, self.pool)
            #game_controller.apply_actions(ai_controller.get_actions())
            self.actions += ctrlr.get_actions()
            
            # save info about the game state after each turn
            self.info_history.append(self.get_info())
    
    
    ################### Game Setup ###################
    def setup(self):
        '''Set up actual game.'''
        self.map = self.generate_random_map()
        self.pool.add_map(self.map)
        locations = self.map.locations()
        
        # set up agents
        for _ in range(self.num_start_warriors):
            for player_id, player in enumerate(self.ai_players):
                
                # create a new agent and add it to the pool
                state = BattleAgentState(self.next_agent_id(), player_id)
                
                # put agent in free, non-blocked location
                loc = random.choice(locations)
                while loc.state.is_blocked or len(loc.agents):
                    loc = random.choice(locations)
                
                self.pool.add_agent(self.next_agent_id(), state, loc.pos)
                
        # spread orbs
        free_loc = set([loc for loc in locations if not loc.state.is_blocked])
        for loc in random.sample(free_loc, int(len(free_loc)*self.food_ratio)):
            loc.state.orbs += 1
    
    def next_agent_id(self):
        self.next_id += 1
        return self.next_id - 1
    
    def generate_random_map(self) -> mase.HexMap:
        '''Generates a random map according to some conditions.'''
        game_map = mase.HexMap(self.map_radius, default_state = BattleLocationState(0, False))
        
        # block off some areas of the map
        random.seed(self.map_seed)
        blocked_pos = random.sample(game_map.positions, int(len(game_map)*self.blocked_ratio))
        for pos in blocked_pos:
            game_map[pos].state.is_blocked = True
        
        return game_map
        
    def get_info(self):
        return {
            #'actions': [a.get_info() for a in self.actions],
            'agents': self.pool.get_info(),
            'map': self.map.get_info(),
        }
        
    def save_game_state(self, fname: str):
        with open(fname, 'w') as f:
            json.dump(self.info_history, f)
        
        
    