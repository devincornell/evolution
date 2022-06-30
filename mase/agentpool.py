import random
import typing
from .errors import *
from .agentstate import AgentID

class AgentPool(dict):
    '''Maintains agents, including scheduler.
    '''
    def add(self, agent_id: AgentID, agent: typing.Any):
        if agent_id in self:
            raise AgentExistsError(f'The agent {agent_id} already exists in this pool.')
        self[agent_id] = agent
        
    def remove(self, agent_id: AgentID):
        try:
            del self[agent_id]
        except KeyError:
            raise AgentDoesNotExistError(f'The agent {agent_id} does not exist in this pool.')


