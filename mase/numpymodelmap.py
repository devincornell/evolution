


import dataclasses
from re import X
import typing
import numpy as np

#from first.agentid import AgentID
from .agent import Agent, AgentID

from .location import Location
from .position import Position

class AgentExistsError(Exception):
    pass

class AgentDoesNotExistError(Exception):
    pass

class OutOfBoundsError(Exception):
    pass

class MovementRuleViolationError(Exception):
    pass

class NumpyModelMap:
    def __init__(self, size_x: int, size_y: int, movement_rule: typing.Callable = None):
        '''
        Args:
            movement_rule: function accepting three arguments: agent, current location, future location.
        '''
        
        # verifies that an agent move is allowed
        self.movement_rule = movement_rule
        
        # add agents
        rows = list()
        for y in range(size_y):
            rows.append([Location(self, Position(x,y)) for x in range(size_x)])

        self.locs: np.ndarray = np.array(rows)
        self.agent_pos: typing.Dict[AgentID, Position] = dict()

    @property
    def size_x(self): return self.locs.shape[1]
    
    @property
    def size_y(self): return self.locs.shape[0]

    def __repr__(self):
        return f'{self.__class__.__name__}(size={self.size_x}x{self.size_y})'
    
    ############################# Working With Locations #############################
    def __getitem__(self, pos: Position):
        '''Get location at desired position.'''
        return self.get_loc(pos)
    
    def __contains__(self, agent_id: AgentID):
        return agent_id in self.locs

    def get_loc(self, pos: Position) -> Location:
        '''Get location at desired position.'''
        self.check_pos(pos)
        return self.locs[pos.y, pos.x]
    
    def check_pos(self, pos: Position) -> None:
        '''Check if position is within map, otherwise raise exception.'''
        if pos.x < 0 or pos.x >= self.size_x or pos.y < 0 or pos.y >= self.size_y:
            raise OutOfBoundsError(f'{pos} is out of bounds for map {self}.')
    
    def region(self, center: Position, dist: int) -> np.ndarray:
        '''Get 2d array of squares within the given distance.'''
        ymin = max(center.y-dist, 0)
        ymax = min(center.y+dist+1, self.locs.shape[0])
        xmin = max(center.x-dist, 0)
        xmax = min(center.x+dist+1, self.locs.shape[1])
        return self.locs[ymin:ymax, xmin:xmax]

    def region_locs(self, center: Position, dist: int, **flatten_kwargs):
        '''Get sequence of locations in the given region.'''
        return self.region(center, dist).flatten(**flatten_kwargs)
    
    ############################# Working With Agents #############################
    def get_agent_pos(self, agent_id: AgentID) -> Position:
        '''Get position of the provided agent.'''
        try:
            return self.agent_pos[agent_id]
        except KeyError:
            raise AgentDoesNotExistError('This agent does not exist on the map.')

    def get_agent_loc(self, agent_id: AgentID) -> Location:
        '''Get the location object associated with teh agent.'''
        return self.get_loc(self.get_agent_pos(agent_id))
        
    def add_agent(self, agent_id: AgentID, pos: Position):
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
        
    def move_agent(self, agent_id: int, agent: Agent, new_pos: Position):
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
        