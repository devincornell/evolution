from __future__ import annotations
import dataclasses
import mase
import typing
import enum
import random
import collections
import json
import copy

class ActionType(enum.Enum):
    MOVE = enum.auto()
    ATTACK = enum.auto()
    CONSUME = enum.auto()
    
class Action:
    pass
    #def get_info(self) -> typing.Dict:
    #    return dataclasses.asdict(self)

@dataclasses.dataclass
class MoveAction(Action):
    agent_id: mase.AgentID
    old_pos: mase.HexPos
    new_pos: mase.HexPos
    action_type: ActionType = ActionType.MOVE
    
    def get_info(self) -> typing.Dict:
        return {
            'action_type': str(self.action_type),
            'agent_id': self.agent_id,
            'new_pos': self.new_pos.coords(),
            'new_pos_xy': (self.new_pos.x, self.new_pos.y),
            'old_pos': self.old_pos.coords(),
            'old_pos_xy': (self.old_pos.x, self.old_pos.y),
        }


@dataclasses.dataclass
class AttackAction(Action):
    agent_id: mase.AgentID
    target_id: mase.AgentID
    target_pos: tuple
    target_pos_xy: tuple
    action_type: ActionType = ActionType.ATTACK
    
    def get_info(self) -> typing.Dict:
        return {
            'action_type': str(self.action_type),
            'agent_id': self.agent_id,
            'target_id': self.target_id,
            'target_pos': self.target_pos,
            'target_pos_xy': self.target_pos_xy,
        }
    
@dataclasses.dataclass
class ConsumeAction(Action):
    agent_id: mase.AgentID
    action_type: ActionType = ActionType.CONSUME

    def get_info(self) -> typing.Dict:
        return {
            'action_type': str(self.action_type),
            'agent_id': self.agent_id,
        }