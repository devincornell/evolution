import dataclasses
import math
import typing
import copy

#from .position import Position
from .position import HexPosition
from .agentstatepool import AgentID

#MapType = typing.TypeVar('MapType')

@dataclasses.dataclass
class LocationState:
    '''Maintains state for each location.'''
    def get_view(self):
        '''Create a copy of itself for sharing with the user.'''
        return copy.deepcopy(self)
    
    def get_info(self):
        '''Get info for data collection.'''
        raise NotImplementedError('Must implement get_info for the LocationState object.')    

class Location:
    __slots__ = ['pos', 'state', 'agents']
    pos: HexPosition
    state: LocationState
    agents: typing.Set[AgentID]

    def __init__(self, pos: HexPosition, state: type = None, agents: typing.Set[AgentID] = None):
        '''
        Args:
            state: custom game state.
        '''
        self.pos = pos
        self.state = copy.copy(state) if state is not None else None
        self.agents = set(copy.copy(agents)) if agents is not None else set()
        
    ############################# Working With Resources #############################    
    def __contains__(self, agent_id: AgentID):
        '''Check if this location contains the agent.'''
        return agent_id in self.agents
        
    ############################# Utility #############################
    #def get_view(self) -> LocationView:
    #    '''Get a view of the current location without any methods.'''
    #    # use deepcopy on state since the game might deside that
    #    return LocationView(self.pos.coords(), self.state.as_view(), self.agents.copy())
    def deepcopy(self):
        return copy.deepcopy(self)
    
    def get_info(self) -> typing.List[dict]:
        '''Get a dict of info about this location.'''
        q, r, s = self.pos.coords()
        return {'q': q, 'r': r, 's': s, 'x': self.pos.x, 'y': self.pos.y, **self.state}
    
    ############################# Working With Agents #############################
    def add_agent(self, agent_id: AgentID):
        '''Adds agent to this location.'''
        self.agents.add(agent_id)
        
    def remove_agent(self, agent_id: AgentID):
        '''Removes agent to this location.'''
        self.agents.remove(agent_id)

#@dataclasses.dataclass
#class LocationView(Location):
#    '''Can be shared with user without modifying original.'''
#    __slots__ = ['pos', 'state', 'agents']
#    pos: typing.Tuple
#    state: LocationState
#    agents: typing.Set[AgentID]
    