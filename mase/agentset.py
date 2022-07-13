from __future__ import annotations

import random
import typing

from .agent import Agent



class AgentSet(typing.List):
    def random_activation(self, team_id: int = None) -> AgentSet:
        '''Get agent ids in a random order.'''
        if team_id is not None:
            agents = [a for a in self if a.state.team_id]
        
        
        return self.__class__(random.sample(subset, len(self)))


