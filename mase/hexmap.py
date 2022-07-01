


import dataclasses
from re import X
import typing
import numpy as np

#from first.agentid import AgentID
from .agentstate import AgentState, AgentID

from .location import Location, LocationView
#from .position import Position
from .cyhexposition import CyHexPosition
from .errors import *

# used for basehexmap where the types of interfaces are different
Position = CyHexPosition

class BaseHexMap:
    '''Methods that appear in both view and full map.'''
    
    ############################# Working With Locations #############################
    def __getitem__(self, pos: Position) -> Location:
        '''Get location at desired position.'''
        try:
            return self.locs[pos]
        except KeyError:
            raise OutOfBoundsError(f'{pos} is out of bounds for map {self}.')
    
    def __iter__(self):
        return iter(self.locs.values())

    def positions(self) -> typing.Set[Position]:
        return set(self.locs.keys())
    
    def locations(self) -> typing.List[Position]:
        return list(self.locs.values())
    
    def check_pos(self, pos: Position) -> None:
        '''Check if position is within map, otherwise raise exception.'''
        if pos in self.locs:
            raise OutOfBoundsError(f'{pos} is out of bounds for map {self}.')
    
    def region(self, center: Position, dist: int) -> set:
        '''Get sequence of positions within the given distance.'''
        return center.neighbors(dist) | set(self.locs.keys())

    def region_locs(self, center: Position, dist: int) -> list:
        '''Get sequence of locations in the given region.'''
        return [self[pos] for pos in self.region(center, dist)]
    
    ############################# Working With Agents #############################
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
        return self.get_loc(self.get_agent_pos(agent_id))
    
    ############################# Other Helpers #############################
    def get_loc_info(self) -> typing.List[dict]:
        '''Get dictionary information about each location.'''
        return [loc.get_info() for loc in self.locs.values()]
    
@dataclasses.dataclass
class HexMapView(BaseHexMap):
    __slots__ = ['locs', 'agent_pos']
    locs: typing.Dict[typing.Tuple, LocationView]
    agent_pos: typing.Dict[AgentID, typing.Tuple]
    
    def pathfind_dfs(self, source: tuple, target: tuple, avoid_positions: typing.Set[tuple]):
        '''Find the first path from source to target using dfs.
        Args:
            avoid_positions: set of positions to avoid when pathfinding.
        '''
        avoidset = {CyHexPosition(*pos) for pos in avoid_positions}
        source_pos, target_pos = CyHexPosition(source), CyHexPosition(target)
        return source_pos.pathfind_dfs(target, avoidset)
        
    def nearest_agents(self, position: tuple):
        '''Get agents nearest to the provided position.'''
        target = CyHexPosition(*position)
        sortkey = lambda pos: target.dist(pos)
        return list(sorted([aid for aid, pos in self.agent_pos.items()], key=sortkey))
        

class HexMap(BaseHexMap):
    locs: typing.Dict[CyHexPosition, Location]
    agent_pos: typing.Dict[AgentID, CyHexPosition]
    
    def __init__(self, radius: int, default_loc_state: typing.Dict = None, movement_rule: typing.Callable = None):
        '''
        Args:
            movement_rule: function accepting three arguments: agent, current location, future location.
        '''
        self.radius = radius
        self.movement_rule = movement_rule

        self.locs = dict()
        self.agent_pos = dict()

        center = CyHexPosition(0, 0, 0)
        valid_pos = center.neighbors(radius)
        valid_pos.add(center)
        self.border_pos = center.neighbors(radius+1) - valid_pos
        for pos in valid_pos:
            self.locs[pos] = Location(pos, self, state=default_loc_state)

    def __repr__(self):
        return f'{self.__class__.__name__}(size={self.radius})'
    
    
    ############################# Views #############################    
    def get_view(self):
        '''Create a view that the user cannot modify.'''
        locs = {pos.coords():loc.get_view() for pos,loc in self.locs.items()}
        agent_pos = {aid:pos.coords() for aid,pos in self.agent_pos.items()}
        return HexMapView(locs=locs, agent_pos=agent_pos)
    
    ############################# Working With Agents #############################    
    def add_agent(self, agent_id: AgentID, pos: CyHexPosition):
        '''Add the agent to the map.'''
        self.check_pos(pos)
        if agent_id in self.agent_pos:
            raise AgentExistsError(f'The agent "{agent_id}" already exists on this map.')
        self.agent_pos[agent_id] = pos
        self.get_loc(pos).agents.append(agent_id)
        
    def remove_agent(self, agent_id):
        '''Remove the agent form the map.'''
        loc = self.get_agent_loc(agent_id)
        loc.agents.remove(agent_id)
        del self.agent_pos[agent_id]
        
    def move_agent(self, agent_id: int, agent: AgentState, new_pos: CyHexPosition):
        '''Move the agent to a new location after checking rule.
        '''        
        old_loc = self.get_agent_loc(agent_id)
        new_loc = self.get_loc(new_pos)
        
        if self.movement_rule is not None:
            if not self.movement_rule(agent, old_loc, new_loc):
                raise MovementRuleViolationError(f'Agent {agent_id} movement from {old_loc.pos} to '
                    f'{new_loc.pos} is invalid according to movement rule.')
                
        old_loc.remove_agent(agent_id)
        new_loc.add_agent(agent_id)
        self.agent_pos[agent_id] = new_pos
        