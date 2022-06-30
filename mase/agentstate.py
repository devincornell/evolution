import typing
import dataclasses

class AgentID(int):
    '''Custom type for agent id (mostly for type hints).'''
    pass

@dataclasses.dataclass
class AgentState:
    '''Represents the state of an agent according to the given game.'''
    pass
