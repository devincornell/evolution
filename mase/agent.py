import typing
import dataclasses

from mase.position.pyhexposition import PyHexPosition

from .errors import *
from .hexmap import HexMap
from .position import HexPosition
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
        p, q, r = self.pos.coords()
        return {
            'id': self.id, 
            #'x': self.pos.x, 
            #'y': self.pos.x, 
            'xy': self.pos.coords_xy(),
            #'p': p, 'q': q, 'r': r,
            'coords': self.pos.coords(),
            **self.state.get_info()
        }
    
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

    def set_map(self, map: HexMap):
        '''Set the map.'''
        self._map = map
    
    @property
    def pos(self) -> HexPosition:
        return self.map.get_agent_pos(self.id)
    
    @property
    def loc(self) -> Location:
        return self.map.get_agent_loc(self.id)
    
    ##################### Utility Functions for User #####################
    
    def nearest_agents(self):
        '''Get agents nearest to this agent after filtering criteria.'''
        #sortkey = lambda pos: self.pos.dist(pos)
        #return [self.pool[aid] for aid in self.map.agents(sortkey) if agent_filter(self.pool[aid])]
        return self.map.nearest_agents(self.pos)

    def nearest_locs(self) -> Locations:
        '''Get locations nearest to this position after filtering criteria.'''
        sortkey = lambda loc: self.pos.dist(loc.pos)
        return self.map.locations(key=sortkey)
    
    def shortest_path(self, target: PyHexPosition):
        '''Get the shortest path between this agent and the target.'''
        return self.map.get_shortest_paths(self.pos, target)

    def pathfind_dfs(self, target: HexPosition, use_positions: typing.Set[HexPosition]):
        '''Find the first path from source to target using dfs.
        Args:
            use_positions: valid movement positions.
        '''
        #useset = {self.map.PositionType(*pos) for pos in use_positions}
        #target_pos = self.map.PositionType(*target)
        return self.pos.pathfind_dfs(target, use_positions)

    def pathfind_dfs_avoid(self, target: tuple, avoid_positions: typing.Set[HexPosition]):
        '''Find the first path from source to target using dfs.
        Args:
            avoid_positions: set of positions to avoid when pathfinding.
        '''
        #avoidset = {self.map.PositionType(*pos) for pos in avoid_positions}
        #target_pos = self.map.PositionType(*target)
        return [pos.coords() for pos in self.pos.pathfind_dfs_avoid(target, avoid_positions)]

