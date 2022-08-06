import random
import collections
import typing
import json

from sklearn import neighbors

#from battlegame import BattleGame
from mase import HexMap, Agent
from .errors import *
from .game import BattleAgentList
from .controller import BattleController


def random_walk_ai(team_id: int, game_map: HexMap, agents: BattleAgentList, ctrlr: BattleController):
    '''Each agent moves to a random nearby location.'''
    #ctrlr.verbose = True
    for agent in agents:
        if agent.state.team_id == team_id:
            
            nearby = agent.neighbor_locs(dist=agent.state.speed)
            potential_locs = [loc for loc in nearby if not loc.num_agents and not loc.state.is_blocked]
            
            if len(potential_locs):
                new_loc = random.choice(potential_locs)
                ctrlr.move(agent, new_loc.pos)


def consume_attack(team_id: int, game_map: HexMap, agents: BattleAgentList, ctrlr: BattleController):
    #ctrlr.verbose = True
    my_agents = [a for a in agents if a.state.team_id == team_id]
    for agent in my_agents:
        
        #print(f'nearest ({agent.id}):', [a.id for a in agent.nearest_agents()])
        
        # if agent is standing on an orb, consume it. otherwise, try to attack
        try:
            attack_closest_if_near(team_id, agent, ctrlr)
            if agent.loc.state.num_orbs > 0:
                ctrlr.consume(agent)
        except OutOfActionsError:
            pass
            
        # the agent can move to any of these positions
        valid_positions = [l.pos for l in game_map.locations() if not l.state.is_blocked and not len(l.agents)]
        
        # check each location that has an orb but no other agents
        for loc in agent.nearest_locations():
            if loc.state.num_orbs > 0 and not len(loc.agents):
                path = agent.pathfind_dfs(loc.pos, valid_positions)
                
                # this means that there is a path
                if path is not None:
                    
                    # compute the number of steps that agent can traverse
                    nsteps = min(agent.state.speed, len(path)-1)
                    ctrlr.move(agent, path[nsteps])
                    break
        
        try:
            attack_closest_if_near(team_id, agent, ctrlr)
            if agent.loc.state.num_orbs > 0:
                ctrlr.consume(agent)
        except OutOfActionsError:
            pass
        

def attack_consume(team_id: int, game_map: HexMap, agents: BattleAgentList, ctrlr: BattleController):
    #ctrlr.verbose = True
    # choose agents in random order so some 
    for agent in agents.from_team(team_id):
        
        # find map positions that are valid for moving to
        valid_positions = {loc.pos for loc in game_map.locations() if not loc.state.is_blocked and not len(loc.agents)}
                    
        # try attacking first, then see if there are any orbs to consume
        try:
            attack_closest_if_near(team_id, agent, ctrlr)
            if agent.loc.state.num_orbs > 0:
                ctrlr.consume(agent)
        except OutOfActionsError:
            pass
        
        for other_agent in agent.nearest_agents():
            if other_agent.state.team_id != team_id:
                    
                path = agent.pathfind_dfs(other_agent.pos, valid_positions)
                if path is not None:
                    path = path[:-1]
                    nsteps = min(agent.state.speed, len(path)-1)
                    
                    if agent.pos != path[nsteps]:
                        ctrlr.move(agent, path[nsteps])
                    break
        
        try:
            attack_closest_if_near(team_id, agent, ctrlr)
            if agent.loc.state.num_orbs > 0:
                ctrlr.consume(agent)
        except OutOfActionsError:
            pass

def attack_closest_if_near(team_id: int, agent: Agent, ctrlr: BattleController):
    for other_agent in agent.nearest_agents():
        if agent.pos.dist(other_agent.pos) == 1 and team_id != other_agent.state.team_id:
            #print('current agents:', [a.id for a in agent.map.agents()])
            #print('target:', other_agent)
            #print('target_pos:', other_agent.pos)
            ctrlr.attack(agent, other_agent)
            break