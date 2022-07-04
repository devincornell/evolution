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
                    
                        
                
#def example_ai_attack(team_id, game_map, pool, controller):
#    for agent in pool.agents:
#        if agent.team_id == team_id:
#            criteria = lambda aid: True
#            nearest = game_map.nearest_agents(game_map.get_agent_pos(agent.id))
#            if loc.state.orbs > 0:
#                # they found some orbs!
#                controller.consume(agent.id)

if __name__ == '__main__':

    game = battlegame.BattleGame(
        ai_players = [example_ai_consume, example_ai_consume],
        map_radius = 10,
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
    