import copy
import itertools
import typing
import igraph
from .position import PyHexPosition
from .location import Location, LocationState
from .errors import *
from .agentid import AgentID

class HexNetMap:
    posmap: typing.Dict[PyHexPosition, igraph.Vertex]
    agent_pos: typing.Dict[AgentID, PyHexPosition]
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

    def __contains__(self, agent_id: AgentID) -> bool:
        '''Check if the agent is on the map.'''
        return agent_id in self.agent_pos
    
    def __iter__(self) -> iter:
        return (v['loc'] for v in self.graph.vs)
    
    def __len__(self) -> int:
        return len(self.locs)

    def __contains__(self, pos: PyHexPosition) -> bool:
        return pos in self.posmap
    
    ############################# Network Vertices #############################    
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
    def __contains__(self, agent_id: AgentID) -> bool:
        '''Check if the agent is on the map.'''
        return agent_id in self.agent_pos
    
    @property
    def agent_ids(self) -> typing.List[AgentID]:
        '''Get locations after filtering and sorting.'''
        return list(self.agent_pos.keys())

    def get_agent_pos(self, agent_id: AgentID) -> PyHexPosition:
        '''Get position of the provided agent.'''
        try:
            return self.agent_pos[agent_id]
        except KeyError:
            raise AgentDoesNotExistError('This agent does not exist on the map.')

    def get_agent_loc(self, agent_id: AgentID) -> Location:
        '''Get the location object associated with the agent.'''
        return self.location(self.get_agent_pos(agent_id))


    ############################# Manipulating Agents #############################

    def move_agent(self, agent_id: AgentID, new_pos: PyHexPosition):
        '''Move the agent to a new location after checking rule.
        '''        
        old_loc = self.get_agent_loc(agent_id)
        new_loc = self[new_pos]
                        
        old_loc.remove_agent(agent_id)
        new_loc.add_agent(agent_id)
        self.agent_pos[agent_id] = new_pos

    def add_agent(self, agent_id: AgentID, pos: PyHexPosition):
        '''Add the agent to the map.'''
        if agent_id in self.agent_pos:
            raise AgentExistsError(f'The agent "{agent_id}" already exists on this map.')
        self.agent_pos[agent_id] = pos
        self.location(pos).add_agent(agent_id)
        
    def remove_agent(self, agent_id: AgentID):
        '''Remove the agent form the map.'''
        loc = self.get_agent_loc(agent_id)
        loc.remove_agent(agent_id)
        del self.agent_pos[agent_id]

    ############################# Helpers #############################



