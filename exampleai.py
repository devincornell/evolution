import random
import collections
import json
import battlecontroller
from battlegameerrors import *
import mase
#from mase import agentstatepool

def consume_attack(team_id: int, game_map: mase.HexMap, agents: mase.AgentPool, controller: battlecontroller.BattleController):
    #blockedset = {loc.pos.coords() for loc in game_map.locations(filter=lambda l: l.state.is_blocked)}
    my_agents = [a for a in agents if a.state.team_id == team_id]
    for agent in my_agents:
        
        # if agent is standing on an orb, consume it. otherwise, try to attack
        try:
            attack_if_near(team_id, agent, controller)
            if agent.loc.state.orbs > 0:
                controller.consume(agent.id)
        except OutOfActionsError:
            pass
            
        # the agent can move to any of these positions
        valid_positions = [loc.pos for loc in game_map.locations(lambda l: not l.state.is_blocked and not len(l.agents))]
        
        # check each location that has an orb but no other agents
        for loc in agent.nearest_locs(lambda l: l.state.orbs > 0 and not len(l.agents)):
            path = agent.pathfind_dfs(loc.pos, valid_positions)
            
            # this means that there is a path
            if path is not None:
                
                # compute the number of steps that agent can traverse
                nsteps = min(agent.state.speed, len(path)-1)
                controller.move(agent.id, path[nsteps])
                break
        
        try:
            attack_if_near(team_id, agent, controller)
            if agent.loc.state.orbs > 0:
                controller.consume(agent.id)
        except OutOfActionsError:
            pass
                    

def attack_consume(team_id: int, game_map: mase.HexMap, agents: mase.AgentPool, controller: battlecontroller.BattleController):
    
    # just get the agents on this team
    for agent in random.sample(list(agents), len(agents)):
        if agent.state.team_id == team_id:
            
            # only some of the map positions are valid to move to
            valid_positions = {loc.pos for loc in game_map.locations(lambda l: not l.state.is_blocked and not len(l.agents))}
                        
            # try to attack before doing anything else
            try:
                attack_if_near(team_id, agent, controller)
                if agent.loc.state.orbs > 0:
                    controller.consume(agent.id)
            except OutOfActionsError:
                pass
            
            for other_agent in agent.nearest_agents(lambda a: a.state.team_id != team_id):
                    
                path = agent.pathfind_dfs(other_agent.pos, valid_positions)
                if path is not None:
                    path = path[:-1]
                    nsteps = min(agent.state.speed, len(path)-1)
                    
                    if agent.pos != path[nsteps]:
                        controller.move(agent.id, path[nsteps])
                    break
            
            try:
                attack_if_near(team_id, agent, controller)
                if agent.loc.state.orbs > 0:
                    controller.consume(agent.id)
            except OutOfActionsError:
                pass

def attack_if_near(team_id: int, agent: mase.Agent, controller: battlecontroller.BattleController):
    for other_agent in agent.nearest_agents(lambda a: a.pos.dist(agent.pos) == 1 and a.state.team_id != team_id):
        controller.attack(agent.id, other_agent.id)
        break