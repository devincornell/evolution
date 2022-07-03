import random
import typing
import copy

from .errors import *
#from .agentstate import AgentID, AgentState

class AgentID(int):
    '''Custom type for agent id (mostly for type hints).'''
    pass

#@dataclasses.dataclass
class AgentState:
    def get_info(self):
        '''Get info dictionary for final game output.'''
        raise NotImplementedError('Must implement get_info for the AgentState object.')

class AgentStatePool(typing.Dict[AgentID, AgentState]):
    '''Keeps track of agent states.
    '''
    ##################### Add/Remove Functions #####################
    def add_agent(self, agent_id: AgentID, agent_state: AgentState):
        if agent_id in self:
            raise AgentExistsError(f'The agent {agent_id} already exists in this pool.')
        self[agent_id] = agent_state
        
    def remove_agent(self, agent_id: AgentID):
        try:
            del self[agent_id]
        except KeyError:
            raise AgentDoesNotExistError(f'The agent {agent_id} does not exist in this pool.')
        
    def get_agent(self, agent_id: AgentID) -> AgentState:
        try:
            return self[agent_id]
        except KeyError:
            raise AgentDoesNotExistError(f'The agent {agent_id} does not exist in this pool.')

    ##################### Activation Functions #####################
    def random_activation(self) -> typing.List[AgentID]:
        '''Get agent ids in a random order.'''
        return list(random.sample(self.keys(), len(self)))
    
    def ordered_activation(self, sort_key: typing.Callable):
        '''Activate agents according to some sorting criteria.'''
        
    ##################### View-Related Functions #####################
    def deepcopy(self):
        return copy.deepcopy(self)
