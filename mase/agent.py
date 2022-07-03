import typing
import dataclasses

from .errors import *
from .hexmap import HexMap
from .position import HexPosition
from .location import Location

#from .agentpool import AgentPool
AgentPoolType = typing.TypeVar('AgentPoolType')

class AgentID(int):
    '''Custom type for agent id (mostly for type hints).'''
    pass

#@dataclasses.dataclass
class AgentState:
    def get_info(self):
        '''Get info dictionary for final game output.'''
        #raise NotImplementedError('Must implement get_info for the AgentState object.')
        #return dataclasses.asdict(self)
        return {}
    
@dataclasses.dataclass
class Agent:
    '''Represents a single agent in the model. Interface over pool and map.'''
    id: AgentID
    state: AgentState
    pool: AgentPoolType
    _map: HexMap
    
    def __pos_init__(self):
        # make sure agent is in map
        pos = self.pos
    
    def __hash__(self):
        '''Unique set by id.'''
        return hash(self.id)
    
    ##################### Map Access Functions #####################
    @property
    def map(self):
        if self._map is not None:
            return self._map
        else:
            raise MapIsNotAttachedError(f'A map was not attached to this {self.__class__.__name__}.')
            
    @property
    def map_attached(self):
        return self._map is not None
    
    @property
    def pos(self) -> HexPosition:
        self.map.get_agent_pos(self.id)
    
    @property
    def loc(self) -> Location:
        self.map.get_agent_loc(self.id)
    
    ##################### Utility Functions for User #####################
    
    def nearest_agents(self, agent_filter: typing.Callable = lambda agent: True) -> typing.List[Agent]:
        '''Get agents nearest to this agent after filtering criteria.'''
        sortkey = lambda pos: self.pos.dist(pos)
        return [self.pool[aid] for aid in self.map.agents(sortkey) if agent_filter(self.pool[aid])]

    def nearest_locs(self, loc_filter: typing.Callable = lambda agent: True) -> typing.List[Location]:
        '''Get locations nearest to this position after filtering criteria.'''
        sortkey = lambda pos: self.pos.dist(pos)
        return self.map.locations(filter=loc_filter, sortkey=sortkey)

    def pathfind_dfs(self, target: tuple, avoid_positions: typing.Set[tuple]):
        '''Find the first path from source to target using dfs.
        Args:
            avoid_positions: set of positions to avoid when pathfinding.
        '''
        avoidset = {self.PositionType(*pos) for pos in avoid_positions}
        source_pos, target_pos = self.map.get_agent_pos(self.pos), self.PositionType(*target)
        return [pos.coords() for pos in source_pos.pathfind_dfs(target_pos, avoidset)]

