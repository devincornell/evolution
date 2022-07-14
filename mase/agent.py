import typing
import dataclasses
import agent

#from mase.position import HexPos

from .errors import *
from .hexmap import HexMap
from .position import HexPos
from .location import Location, Locations
from .agentid import AgentID
#from .hexnetmap import HexNetMap
#from .agentpool import AgentPool
AgentPoolType = typing.TypeVar('AgentPoolType')
#HexMapType = typing.TypeVar('HexMapType')



#@dataclasses.dataclass
class AgentState:
    def get_info(self):
        '''Get info dictionary for final game output.'''
        raise NotImplementedError('Must implement get_info for the AgentState object.')
    
@dataclasses.dataclass
class Agent:
    '''Represents a single agent in the model. Interface over pool and map.'''
    id: AgentID
    state: AgentState
    _map: HexMap = None
    
    def __pos_init__(self):
        # make sure agent is in map
        pos = self.pos
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def get_info(self) -> typing.Dict:
        return {
            'id': self.id, 
            'xy': self.pos.coords_xy(),
            'pqr': self.pos.coords(),
            **self.state.get_info()
        }
    
    ##################### Map Access Functions #####################
    @property
    def map(self):
        '''Access the attached map or raise exception. For internal use.'''
        if self._map is not None:
            return self._map
        else:
            raise MapIsNotAttachedError(f'A map was not attached to this {self.__class__.__name__}.')
            
    @property
    def map_attached(self):
        '''Check if map is attached. For internal use.'''
        return self._map is not None

    def set_map(self, map: HexMap):
        '''Set reference to a map. For internal use.'''
        self._map = map
    
    @property
    def pos(self) -> HexPos:
        '''Agents current position.'''
        return self.map.agent_pos(self.id)
    
    @property
    def loc(self) -> Location:
        '''Location at Agents current position.'''
        return self.map.agent_loc(self.id)
    
    ##################### Utility Functions for User #####################
    def nearest_agents(self):
        '''Get agents nearest to this agent after filtering criteria.'''
        return self.map.nearest_agents(self.pos)

    def nearest_locations(self) -> Locations:
        '''Get locations nearest to this agent.'''
        sortkey = lambda loc: self.pos.dist(loc.pos)
        return self.map.locations(key=sortkey)
    
    def shortest_path(self, target: HexPos):
        '''Get the shortest path between this agent and the target position.'''
        return self.map.get_shortest_paths(self.pos, target)
    
    ##################### Outdated Pathfinding Functions #####################
    def depric_pathfind_dfs(self, target: HexPos, use_positions: typing.Set[HexPos]):
        '''Find the first path from source to target using dfs.
        Args:
            use_positions: valid movement positions.
        '''
        return self.pos.pathfind_dfs(target, use_positions)

    def depric_pathfind_dfs_avoid(self, target: tuple, avoid_positions: typing.Set[HexPos]):
        '''Find the first path from source to target using dfs.
        Args:
            avoid_positions: set of positions to avoid when pathfinding.
        '''
        return [pos.coords() for pos in self.pos.pathfind_dfs_avoid(target, avoid_positions)]


class AgentSet(typing.Set[Agent]):
    def random_activation(self) -> typing.List[Agent]:
        '''Get agents in a random order.'''        
        return list(random.sample(list(self), len(self)))


