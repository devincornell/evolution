import typing
import collections
import dataclasses
from typing import List
import mase
 
from battlegameerrors import *

import enum

class ActionType(enum.Enum):
    MOVE = enum.auto()
    ATTACK = enum.auto()
    CONSUME = enum.auto()
    
class Action:
    def get_info(self) -> typing.Dict:
        return dataclasses.asdict(self)

@dataclasses.dataclass
class MoveAction(Action):
    agent_id: mase.AgentID
    new_pos: tuple
    action_type: ActionType = ActionType.MOVE

@dataclasses.dataclass
class AttackAction(Action):
    agent_id: mase.AgentID
    target_id: mase.AgentID
    action_type: ActionType = ActionType.ATTACK
    
@dataclasses.dataclass
class ConsumeAction(Action):
    agent_id: mase.AgentID
    action_type: ActionType = ActionType.CONSUME



@dataclasses.dataclass
class BattleController:
    '''This acts like the "Controller" for the game.'''
    team_id: int
    map: mase.HexMap
    pool: mase.AgentStatePool
    action_sequence: list = dataclasses.field(default_factory=list)
    move_ct: collections.Counter = dataclasses.field(default_factory=collections.Counter)
    action_ct: collections.Counter = dataclasses.field(default_factory=collections.Counter)
    verbose: bool = False
    
    def move(self, agent_id: mase.AgentID, new_position: tuple):
        '''Move the agent to a new position.'''
        agent = self.pool.get_agent(agent_id)
        current_pos = self.map.get_agent_pos(agent_id)
        pos = mase.HexPosition(*new_position)
        loc = self.map[pos]
        
        # do some error checking
        if self.move_ct[agent_id] > 0:
            raise OutOfMovesError('Agent {agent_id} has already moved this turn.')
        elif self.team_id != agent.team_id:
            raise CannotControlOtherTeamMemberError(f'You cannot move a member of another team. '
                f'You are team {self.team_id} but agent {agent_id} is on team {agent.team_id}.')
        elif len(loc.agents):
            existing_agent = list(loc.agents)[0]
            raise AgentAlreadyExistsInLocationError(f'Cannot move agent {agent_id}: '
                f'agent {existing_agent} already exists at {pos}.')
        elif loc.is_blocked:
            raise LocationIsBlockedError(f'Agent {agent_id} cannot move to position {pos}: '
                'it is blocked.')
        elif current_pos.dist(pos) > self.pool.get_agent(agent_id).speed:
            raise OutOfRangeError(f'Agent {agent_id} cannot move to position {pos} because '
                f'it is distance {current_pos.dist(pos)} but agent speed is only '
                f'{self.pool.get_agent(agent_id).speed}.')
        
        self.map.move_agent(agent_id, pos)
        self.action_sequence.append(MoveAction(agent_id, pos))
        self.move_ct[agent_id] += 1
        if self.verbose: print(f'Agent {agent_id} moved {current_pos.dist(pos)} positions to {pos}.')
        
    def attack(self, agent_id: mase.AgentID, target_id: mase.AgentID):
        '''Attack an agent of the opposite team.'''
        agent = self.pool.get_agent(agent_id)
        target_agent = self.pool.get_agent(target_id)
        
        pos = self.map.get_agent_pos(agent_id)
        target_pos = self.map.get_agent_pos(target_id)
        
        # do some error checking
        self.check_action(agent_id)
        if pos.dist(target_pos) > 1:
            raise OutOfRangeError('Agent {agent_id} cannot attack agent {target_id} because it is more than '
                'one cell away.')

        # apply attack
        target_agent.health -= agent.attack
        
        if target_agent.health <= 0:
            self.pool.remove_agent(target_agent.id)
            self.map.remove_agent(target_agent.id)
            agent.health += 1
            if self.verbose: print(f'Agent {agent_id} killed {target_id}: {agent} vs {target_agent}.')
        else:
            if self.verbose: print(f'Agent {agent_id} attacked {target_id}, reducing '
                f'health by {agent.attack} to {target_agent.health}.')
        
        self.action_ct[agent_id] += 1    
        self.action_sequence.append(AttackAction(agent_id, target_id=target_id))
        
        
    def consume(self, agent_id: mase.AgentID):
        '''Agent can collect an orb from the location at it's current position.'''
        loc = self.map.get_agent_loc(agent_id)
        agent = self.pool.get_agent(agent_id)
        
        self.check_action(agent_id)
        if not loc.state.orbs > 0:
            raise NoOrbsAtLocationError(f'There are no orbs at the location of {agent_id}.')
        
        loc.state.orbs -= 1
        agent.level += 1
        agent.health += 1
        
        self.action_ct[agent_id] += 1    
        self.action_sequence.append(ConsumeAction(agent_id))
        if self.verbose: print(f'Agent {agent_id} consumed 1 orb at location {loc.state}.')
        
    def check_action(self, agent_id: mase.AgentID):
        '''Make sure the agent can take another action.'''
        agent = self.pool.get_agent(agent_id)
        if self.action_ct[agent_id] > 0:
            raise OutOfActionsError('Agent {agent_id} has already taken an action this turn.')
        elif self.team_id != agent.team_id:
            raise CannotControlOtherTeamMemberError(f'You cannot order a member of another team to attack. '
                f'You are team {self.team_id} but agent {agent_id} is on team {agent.team_id}.')
    
    def get_actions(self) -> typing.List[Action]:
        return self.action_sequence.copy()
    
    def apply_actions(self, actions: List[Action]):
        '''Apply the actions to this game state.'''
        for action in actions:
            if action.action_type is ActionType.MOVE:
                self.move(action.agent_id, action.new_pos)
            elif action.action_type is ActionType.ATTACK:
                self.attack(action.agent_id, action.target_id)
            elif action.action_type is ActionType.CONSUME:
                self.consume(action.agent_id)
            else:
                raise ActionNotRecognizedError(f'The action {action} was not recognized by the controller.')
    
            
            