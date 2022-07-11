import copy
import itertools
import typing
import igraph
from .position import PyHexPosition
from .location import Locations, Location, LocationState
from .errors import *
#from .agentid import AgentID
from .agent import Agent

class HexNetMap:
    posmap: typing.Dict[PyHexPosition, igraph.Vertex]
    agent_pos: typing.Dict[Agent, PyHexPosition]

    def __init__(self, radius: int, default_state: LocationState = None):
        self.radius = radius
        self.agent_pos = dict()

        # get set of positions
        self.center = PyHexPosition(0, 0, 0)
        all_pos = [self.center] + list(self.center.neighbors(radius))
        
        # create new graph
        self.graph = igraph.Graph(directed=False)
        self.graph.add_vertices(len(all_pos))
        
        # use locations as graph attributes
        locs = [Location(pos, state=copy.deepcopy(default_state)) for pos in all_pos]        
        self.graph.vs['loc'] = locs
        
        # create map from postiions to vertices
        self.posmap = {pos:v for pos,v in zip(all_pos, self.graph.vs)}

    ############################# Dunders #############################    

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(size={self.radius})'

    def __getitem__(self, pos: PyHexPosition) -> Location:
        return self.location(pos)

    def __contains__(self, agent: Agent) -> bool:
        '''Check if the agent is on the map.'''
        return agent in self.agent_pos
    
    def __iter__(self) -> iter:
        return (v['loc'] for v in self.graph.vs)
    
    def __len__(self) -> int:
        return len(self.locs)

    def __contains__(self, pos: PyHexPosition) -> bool:
        return pos in self.posmap
    
    ############################# Vertices and Locations #############################    
    def locations(self) -> Locations:
        return Locations([v['loc'] for v in self.graph.vs])
    
    def location(self, pos: PyHexPosition) -> Location:
        '''Get location at the desired position.'''
        return self.vertex(pos)['loc']

    def vertex(self, pos: PyHexPosition) -> igraph.Vertex:
        '''Get vertex from position.'''
        try:
            return self.posmap[pos]
        except KeyError:
            raise OutOfBoundsError(f'The position {pos} is outside this map.')
    
    def vertex_from_coords(self, coords: tuple) -> igraph.Vertex:
        '''Get vertex from the given coords.'''
        return self.vertex(PyHexPosition(*coords))

    ############################# Accessing Agent Locations #############################
    def __contains__(self, agent: Agent) -> bool:
        '''Check if the agent is on the map.'''
        return agent in self.agent_pos
    
    @property
    def agents(self) -> typing.List[Agent]:
        '''Get locations after filtering and sorting.'''
        return list(self.agent_pos.keys())

    def get_agent_pos(self, agent: Agent) -> PyHexPosition:
        '''Get position of the provided agent.'''
        try:
            return self.agent_pos[agent]
        except KeyError:
            raise AgentDoesNotExistError('This agent does not exist on the map.')

    def get_agent_loc(self, agent: Agent) -> Location:
        '''Get the location object associated with the agent.'''
        return self.location(self.get_agent_pos(agent))


    ############################# Manipulating Agents #############################

    def move_agent(self, agent: Agent, new_pos: PyHexPosition):
        '''Move the agent to a new location after checking rule.
        '''        
        old_loc = self.get_agent_loc(agent)
        new_loc = self[new_pos]
                        
        old_loc.remove_agent(agent)
        new_loc.add_agent(agent)
        self.agent_pos[agent] = new_pos

    def add_agent(self, agent: Agent, pos: PyHexPosition):
        '''Add the agent to the map.'''
        if agent in self.agent_pos:
            raise AgentExistsError(f'The agent "{agent}" already exists on this map.')
        self.agent_pos[agent] = pos
        self.location(pos).add_agent(agent)
        
    def remove_agent(self, agent: Agent):
        '''Remove the agent form the map.'''
        loc = self.get_agent_loc(agent)
        loc.remove_agent(agent)
        del self.agent_pos[agent]

    ############################# Helpers #############################



