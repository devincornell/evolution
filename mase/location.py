import dataclasses
import math
import typing
import copy

#from .position import Position
from .cyhexposition import CyHexPosition
from .agentstate import AgentID

MapType = typing.TypeVar('MapType')

class BaseLocation:
    '''Include methods that appear in both the view and the object.'''
    
    ############################# Working With Resources #############################
    def __getitem__(self, key: typing.Any):
        '''Get a resource attribute.'''
        return self.state[key]
    
    def __contains__(self, agent_id: AgentID):
        '''Check if this location contains the agent.'''
        return agent_id in self.agents


@dataclasses.dataclass
class LocationView(BaseLocation):
    '''Can be shared with user without modifying original.'''
    __slots__ = ['pos', 'state', 'agents']
    pos: typing.Tuple
    state: typing.Dict
    agents: typing.Set[AgentID]


class Location(BaseLocation):
    __slots__ = ['pos', 'map', 'state', 'agents']
    pos: CyHexPosition
    map: MapType
    state: typing.Dict
    agents: typing.Set[AgentID]

    def __init__(self, pos: CyHexPosition, map: MapType, state: typing.Dict = None, agents: typing.Set[AgentID] = None):
        self.pos = pos
        self.map = map
        self.state = state.copy() if state is not None else {}
        self.agents = agents.copy() if agents is not None else set()
        
    ############################# Utility #############################
    def get_view(self) -> LocationView:
        '''Get a view of the current location without any methods.'''
        # use deepcopy on state since the game might deside that
        return LocationView(self.pos.coords(), copy.deepcopy(self.state.copy()), self.agents.copy())
    
    ############################# Working With Agents #############################
    def add_agent(self, agent_id: AgentID):
        '''Adds agent to this location.'''
        self.agents.add(agent_id)
        
    def remove_agent(self, agent_id: AgentID):
        '''Removes agent to this location.'''
        self.agents.remove(agent_id)

    