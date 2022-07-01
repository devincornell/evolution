import dataclasses
import mase
import typing
import enum

class ActionType(enum.Enum):
    MOVE = enum.auto()
    ATTACK = enum.auto()
    EAT = enum.auto()

class Action:
    pass
    
@dataclasses.dataclass
class AttackAction(Action):
    '''Have your agent attack another agent.'''
    agent_id: mase.AgentID
    target_pos: typing.Tuple
    action_type: Action = ActionType.MOVE
    
@dataclasses.dataclass
class AttackAction(Action):
    '''Have your agent attack another agent.'''
    agent_id: mase.AgentID
    target_id: mase.AgentID
    action_type: Action = ActionType.ATTACK
    
@dataclasses.dataclass
class EatAction(Action):
    '''Have your agent eat resources at a particular location.'''
    agent_id: mase.AgentID
    target_pos: typing.Tuple
    action_type: Action = ActionType.EAT
