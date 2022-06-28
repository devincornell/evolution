


import dataclasses
from re import X
import typing
import numpy as np

#from first.agentid import AgentID
from .agent import Agent, AgentID

from .location import Location
#from .position import Position
from .cyhexposition import CyHexPosition

class AgentExistsError(Exception):
    pass

class AgentDoesNotExistError(Exception):
    pass

class OutOfBoundsError(Exception):
    pass

class MovementRuleViolationError(Exception):
    pass

class HexMap:
    def __init__(self, radius: int, default_loc_state: typing.Dict = None, movement_rule: typing.Callable = None):
        '''
        Args:
            movement_rule: function accepting three arguments: agent, current location, future location.
        '''
        self.radius = radius
        self.movement_rule = movement_rule

        self.locs: typing.Dict[CyHexPosition, Location] = dict()
        self.agent_pos: typing.Dict[AgentID, CyHexPosition] = dict()

        center = CyHexPosition(0, 0, 0)
        valid_pos = center.neighbors(radius)
        self.border_pos = center.neighbors(radius+1) - valid_pos
        for pos in valid_pos:
            self.locs[pos] = Location(pos, self, state=default_loc_state)

    def __repr__(self):
        return f'{self.__class__.__name__}(size={self.radius})'
    
    ############################# Working With Locations #############################
    def __getitem__(self, pos: CyHexPosition) -> Location:
        '''Get location at desired position.'''
        try:
            return self.locs[pos]
        except KeyError:
            raise OutOfBoundsError(f'{pos} is out of bounds for map {self}.')
    
    def __contains__(self, agent_id: AgentID):
        return agent_id in self.agent_pos

    def __iter__(self):
        return iter(self.locs.values())

    def positions(self) -> typing.Set[CyHexPosition]:
        return set(self.locs.keys())
    
    def check_pos(self, pos: CyHexPosition) -> None:
        '''Check if position is within map, otherwise raise exception.'''
        if pos in self.locs:
            raise OutOfBoundsError(f'{pos} is out of bounds for map {self}.')
    
    def region(self, center: CyHexPosition, dist: int) -> np.ndarray:
        '''Get 2d array of squares within the given distance.'''
        #rng = list(range(-dist, dist+1))
        #x, y = center.x, center.y
        #return [self[CyHexPosition(x+xd,y+yd)] for xd in rng for yd in rng]
        return center.neighbors(dist) | set(self.locs.keys())

    def region_locs(self, center: CyHexPosition, dist: int):
        '''Get sequence of locations in the given region.'''
        #return self.region(center, dist).flatten(**flatten_kwargs)
        return [self[pos] for pos in self.region(center, dist)]

    def get_loc_info(self) -> typing.List[dict]:
        loc_states = list()
        for pos, loc in self.locs.items():
            q, r, s = pos.as_tuple()
            loc_states.append({
                'q': q, 'r': r, 's': s, 'x': pos.x, 'y': pos.y,
                **loc.state,
            })
        return loc_states

    
    ############################# Working With Agents #############################
    def get_agent_pos(self, agent_id: AgentID) -> CyHexPosition:
        '''Get position of the provided agent.'''
        try:
            return self.agent_pos[agent_id]
        except KeyError:
            raise AgentDoesNotExistError('This agent does not exist on the map.')

    def get_agent_loc(self, agent_id: AgentID) -> Location:
        '''Get the location object associated with teh agent.'''
        return self.get_loc(self.get_agent_pos(agent_id))
        
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
        
    def move_agent(self, agent_id: int, agent: Agent, new_pos: CyHexPosition):
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
        