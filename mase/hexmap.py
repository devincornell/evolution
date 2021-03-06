import copy
import dataclasses
import typing
import numpy as np

#from first.agentid import AgentID
from .agentstatepool import AgentID

from .location import Location, LocationState
from .position import HexPosition
from .errors import *

class HexMap:
    locs: typing.Dict[HexPosition, Location]
    agent_pos: typing.Dict[AgentID, HexPosition]
    
    def __init__(self, radius: int, default_state: LocationState = None, PositionType: type = HexPosition):
        '''
        Args:
            movement_rule: function accepting three arguments: agent, current location, future location.
        '''
        self.radius = radius
        self.PositionType = PositionType

        self.locs = dict()
        self.agent_pos = dict()

        center = self.PositionType(0, 0, 0)
        valid_pos = center.neighbors(radius)
        valid_pos.add(center)
        self.border_pos = center.neighbors(radius+1) - valid_pos
        for pos in valid_pos:
            self.locs[pos] = Location(pos, state=copy.deepcopy(default_state))

    def __repr__(self):
        return f'{self.__class__.__name__}(size={self.radius})'
    
    
    ############################# Views #############################    
    #def get_view(self):
    #    '''Create a view that the user cannot modify.'''
    #    locs = {pos.coords():loc.get_view() for pos,loc in self.locs.items()}
    #    agent_pos = {aid:pos.coords() for aid,pos in self.agent_pos.items()}
    #    return HexMapView(locs=locs, agent_pos=agent_pos, PositionType=self.PositionType)
    def deepcopy(self):
        return copy.deepcopy(self)
    
    ############################# Working With Agents #############################    
    def add_agent(self, agent_id: AgentID, pos: HexPosition):
        '''Add the agent to the map.'''
        self.check_pos(pos)
        if agent_id in self.agent_pos:
            raise AgentExistsError(f'The agent "{agent_id}" already exists on this map.')
        self.agent_pos[agent_id] = pos
        self.locs[pos].agents.add(agent_id)
        
    def remove_agent(self, agent_id: AgentID):
        '''Remove the agent form the map.'''
        loc = self.get_agent_loc(agent_id)
        loc.agents.remove(agent_id)
        del self.agent_pos[agent_id]
        
    def move_agent(self, agent_id: AgentID, new_pos: HexPosition):
        '''Move the agent to a new location after checking rule.
        '''        
        old_loc = self.get_agent_loc(agent_id)
        new_loc = self[new_pos]
                        
        old_loc.remove_agent(agent_id)
        new_loc.add_agent(agent_id)
        self.agent_pos[agent_id] = new_pos
        
    ############################# Working With Locations #############################
    def __getitem__(self, pos: HexPosition) -> Location:
        '''Get location at desired position.'''
        try:
            return self.locs[pos]
        except KeyError:
            raise OutOfBoundsError(f'{pos} is out of bounds for map {self}.')
    
    def __iter__(self):
        return iter(self.locs.values())
    
    def __len__(self):
        return len(self.locs)

    @property
    def positions(self) -> typing.Set[HexPosition]:
        return set(self.locs.keys())
    
    def locations(self, filter: typing.Callable = lambda loc: True, sortkey: typing.Callable = lambda loc: 0) -> typing.List[HexPosition]:
        '''Get locations after filtering and sorting.'''
        return [loc for loc in sorted(self.values(), key=sortkey) if filter(loc)]
    
    def check_pos(self, pos: HexPosition) -> None:
        '''Check if position is within map, otherwise raise exception.'''
        if pos not in self.locs:
            raise OutOfBoundsError(f'{pos} is out of bounds for map {self}.')
    
    def region(self, center: HexPosition, dist: int) -> set:
        '''Get sequence of positions within the given distance.'''
        return center.neighbors(dist) & set(self.locs.keys())

    def region_locs(self, center: HexPosition, dist: int) -> list:
        '''Get sequence of locations in the given region.'''
        return [self[pos] for pos in self.region(center, dist)]
    
    ############################# Working With Agents #############################
    def agents(self, sortkey: typing.Callable = lambda loc: 0) -> typing.List[AgentID]:
        '''Get locations after filtering and sorting.'''
        return [aid for aid,pos in sorted(self.agent_pos.items(), key=lambda a,p: sortkey(self[p]))]

    def __contains__(self, agent_id: AgentID):
        '''Check if the agent is on the map.'''
        return agent_id in self.agent_pos
    
    def get_agent_pos(self, agent_id: AgentID):
        '''Get position of the provided agent.'''
        try:
            return self.agent_pos[agent_id]
        except KeyError:
            raise AgentDoesNotExistError('This agent does not exist on the map.')

    def get_agent_loc(self, agent_id: AgentID) -> Location:
        '''Get the location object associated with teh agent.'''
        return self[self.get_agent_pos(agent_id)]
    
    ############################# Other Helpers #############################
    def get_info(self) -> typing.List[dict]:
        '''Get dictionary information about each location.'''
        return [loc.get_info() for loc in self.locs.values()]
    
    