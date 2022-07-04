import random
import collections

import battlegame
import battlecontroller
from battlegameerrors import *
import mase
#from mase import agentstatepool

def example_ai_consume(team_id: int, game_map: mase.HexMap, agents: mase.AgentPool, controller: battlecontroller.BattleController):
    #blockedset = {loc.pos.coords() for loc in game_map.locations(filter=lambda l: l.state.is_blocked)}
    for agent in agents:
        if agent.state.team_id == team_id:
            valid_positions = [loc.pos for loc in game_map.locations(lambda l: not l.state.is_blocked and not len(l.agents))]
            if agent.loc.state.orbs > 0:
                controller.consume(agent.id)
            
            for loc in agent.nearest_locs(lambda l: l.state.orbs > 0 and not len(l.agents)):
                path = agent.pathfind_dfs(loc.pos, valid_positions)
                if path is not None:
                    nsteps = min(agent.state.speed, len(path)-1)
                    controller.move(agent.id, path[nsteps])
                    break
            
            try:
                if agent.loc.state.orbs > 0:
                    controller.consume(agent.id)
            except OutOfActionsError:
                pass
                    
def attack_if_near(team_id: int, agent: mase.Agent, controller: battlecontroller.BattleController):
    for other_agent in agent.nearest_agents(lambda a: a.pos.dist(agent.pos) == 1 and a.state.team_id != team_id):
        #if other_agent.id in controller.map:
        controller.attack(agent.id, other_agent.id)
        break

def example_ai_attack(team_id: int, game_map: mase.HexMap, agents: mase.AgentPool, controller: battlecontroller.BattleController):
    #blockedset = {loc.pos.coords() for loc in game_map.locations(filter=lambda l: l.state.is_blocked)}
    for agent in random.sample(list(agents), len(agents)):
        if agent.state.team_id == team_id:
            # valid positions change every time
            valid_positions = {loc.pos for loc in game_map.locations(lambda l: not l.state.is_blocked and not len(l.agents))}
            #if agent.pos in valid_positions:
            #    valid_positions.remove(agent.pos)
            
            # attack an enemy if they're near
            attack_if_near(team_id, agent, controller)
            
            for other_agent in agent.nearest_agents(lambda a: a.state.team_id != team_id):
                    
                path = agent.pathfind_dfs(other_agent.pos, valid_positions)[:-1]
                if path is not None:
                    nsteps = min(agent.state.speed, len(path)-1)
                    
                    if agent.pos != path[nsteps]:
                        controller.move(agent.id, path[nsteps])
                    break
            
            try:
                attack_if_near(team_id, agent, controller)
            except OutOfActionsError:
                pass



if __name__ == '__main__':

    game = battlegame.BattleGame(
        ai_players = [example_ai_consume, example_ai_attack],
        map_radius = 6,
        blocked_ratio = 0.2,
        food_ratio = 0.1,
        num_start_warriors = 3,
        map_seed=0, 
        max_turns=100,
    )
    #print(game.pool.get_info())
    #for aid, agent in game.pool.get_info().items():
    #    print(type(aid))
    #exit()
    i = 1
    while not game.is_finished:
        #print(f'Starting turn {i}.')
        game.step()
        i += 1
        if i > game.max_turns:
            break

        # print some data about the results
        agent_levels = dict()
        agent_health = dict()
        for agent in game.pool:
            agent_levels.setdefault(agent.state.team_id, [])
            agent_levels[agent.state.team_id].append(agent.state.level)
            
            agent_health.setdefault(agent.state.team_id, [])
            agent_health[agent.state.team_id].append(agent.state.health)
        
        print(agent_health)
        print(agent_levels)
        #print('==========================')
        #print(len(game.pool.agents))
        #from functools import reduce
        #print(reduce(lambda s1, s2: s1 | s2, [loc.agents for loc in game.map.locations]))
        #print(game.map.get_agent_loc(0))
    game.save_game_state('tmp/save_game1.json')
    
    # make sure the characters ever jumped
    for action in game.actions:
        if action.action_type == battlecontroller.ActionType.MOVE:
            assert(action.old_pos.dist(action.new_pos) == 1)
            #print(action)
    