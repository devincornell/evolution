import dataclasses
import math
import typing

#from .resource import Resource
#from .agent import Agent
from .position import Position
from .agent import AgentID

MapType = typing.TypeVar('MapType')

@dataclasses.dataclass
class Location:
    #__slots__ = ['pos', 'map', 'state', 'agents']
    pos: Position
    map: MapType
    state: typing.Dict = dataclasses.field(default_factory=dict)
    agents: typing.Set[AgentID] = dataclasses.field(default_factory=set)
    
    ############################# Working With Agents #############################
    def add_agent(self, agent_id: AgentID):
        '''Adds agent to this location.'''
        self.agents.add(agent_id)
        
    def remove_agent(self, agent_id: AgentID):
        '''Removes agent to this location.'''
        self.agents.remove(agent_id)
        
    def get_agent(self, agent_id: AgentID):
        '''Get agent by id.'''
        return self.agents[agent_id]
    
    def __contains__(self, agent_id: AgentID):
        '''Check if this location contains the agent.'''
        return agent_id in self.agents
    
    ############################# Working With Resources #############################
    def __getitem__(self, key: typing.Any):
        '''Get a resource attribute.'''
        return self.state[key]
