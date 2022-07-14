import typing
import collections
import dataclasses
from typing import List
import mase
 
from battlegameerrors import *

import enum
from mase.agent import Agent

from mase.agentid import AgentID

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

@dataclasses.dataclass
class BattleController:
    '''This acts like the "Controller" for the game.'''
    team_id: int
    map: mase.HexMap
    #pool: mase.AgentStatePool
    agent_lookup: typing.Dict[AgentID,Agent] = dataclasses.field(default_factory=dict)
    action_sequence: list = dataclasses.field(default_factory=list)
    move_ct: collections.Counter = dataclasses.field(default_factory=collections.Counter)
    action_ct: collections.Counter = dataclasses.field(default_factory=collections.Counter)
    verbose: bool = False
    
    def __post_init__(self):
        self.agent_lookup = {a.id:a for a in self.map.agents}
    
    def move(self, agent: mase.Agent, new_position: mase):
        '''Move the agent to a new position.'''
        new_loc = self.map[new_position]
        
        # do some error checking
        self.check_control(agent)
        if self.move_ct[agent] > 0:
            raise OutOfMovesError(f'Agent {agent.id} has already moved this turn.')
        elif len(agent.loc.agents):
            existing_agent = list(new_loc.agents)[0]
            raise AgentAlreadyExistsInLocationError(f'Cannot move agent {agent.id}: '
                f'agent {existing_agent} already exists at {new_position}.')
        elif new_loc.state.is_blocked:
            raise LocationIsBlockedError(f'Agent {agent.id} cannot move to position {new_position}: '
                'it is blocked.')
        elif agent.pos.dist(new_position) > agent.state.speed:
            raise OutOfRangeError(f'Agent {agent.id} cannot move to position {new_position} because '
                f'it is distance {agent.pos.dist(new_position)} but agent speed is only '
                f'{agent.state.speed}.')
        
        self.map.move_agent(agent, new_position)
        self.action_sequence.append(MoveAction(agent.id, agent.pos, new_position))
        self.move_ct[agent] += 1
        if self.verbose: print(f'Agent {agent.id} moved {agent.pos.dist(new_position)} positions to {new_position}.')
        
    def attack(self, agent: mase.Agent, target: mase.Agent):
        '''Attack an agent of the opposite team.'''
        
        # do some error checking
        self.check_control(agent)
        self.check_action(agent)
        if agent.pos.dist(target.pos) > 1:
            raise OutOfRangeError(f'Agent {agent.id} cannot attack agent {target.id} because it is more than '
                'one cell away.')

        # apply attack
        target.state.health -= agent.state.attack
        
        if target.state.health <= 0:
            self.agent_lookup.remove_agent(target.id)
            #self.map.remove_agent(target_agent.id)
            agent.state.health += 1
            if self.verbose: print(f'Agent {agent.id} killed {target.id}: {agent} vs {target}.')
        else:
            if self.verbose: print(f'Agent {agent.id} attacked {target.id}, reducing '
                f'health by {agent.state.attack} to {target.state.health}.')
        
        self.action_ct[agent] += 1
        action = AttackAction(agent.id, target_id=target.id, target_pos=target.pos.coords(), target_pos_xy=target.pos.coords_xy())
        self.action_sequence.append(action)
        
        
    def consume(self, agent: mase.Agent):
        '''Agent can collect an orb from the location at it's current position.'''
        
        self.check_control(agent)
        self.check_action(agent)
        if not agent.loc.state.num_orbs > 0:
            raise NoOrbsAtLocationError(f'There are no orbs at agent {agent.id}\'s location: {agent.loc}.')
        
        agent.loc.state.num_orbs -= 1
        agent.state.level += 1
        agent.state.health += 1
        
        self.action_ct[agent] += 1
        self.action_sequence.append(ConsumeAction(agent.id))
        if self.verbose: print(f'Agent {agent.id} consumed 1 orb at location {agent.loc.state}.')
        
    def check_action(self, agent: mase.Agent):
        '''Make sure the agent can take another action.'''
        if self.action_ct[agent] > 0:
            raise OutOfActionsError(f'Agent {agent.id} has already taken an action this turn.')
            
    def check_control(self, agent: mase.Agent):
        '''Check if user can control the given agent.'''
        if self.team_id != agent.state.team_id:
            raise CannotControlOtherTeamMemberError(f'You cannot order a member of another team to attack. '
                f'You are team {self.team_id} but agent {agent.id} is on team {agent.state.team_id}.')
        elif agent not in self.map:
            raise AgentHasBeenKilledError(f'Agent {agent.id} does not exist on the map. '
                f'It has likely been killed.')
    
    def get_actions(self) -> typing.List[Action]:
        return self.action_sequence.copy()
    
    def apply_actions(self, actions: List[Action]):
        '''Apply the actions to this game state.'''
        for action in actions:
            if action.action_type is ActionType.MOVE:
                agent = self.agent_lookup[action.agent_id]
                self.move(agent, action.new_pos)
            elif action.action_type is ActionType.ATTACK:
                agent = self.agent_lookup[action.agent_id]
                target = self.agent_lookup[action.target_id]
                self.attack(agent, target)
            elif action.action_type is ActionType.CONSUME:
                agent = self.agent_lookup[action.agent_id]
                self.consume(agent)
            else:
                raise ActionNotRecognizedError(f'The action {action} was not recognized by the controller.')
    
            
            