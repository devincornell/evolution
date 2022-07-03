import random
import collections

import battlegame
import battlecontroller
import mase
from mase import agentstatepool

def example_ai(team_id: int, game_map: mase.HexMap, pool: mase.AgentStatePool, controller: battlecontroller.BattleController):
    #print(f'Starting team {team_id} turn!')
    for agent in pool.agents:
        if agent.team_id == team_id:
            loc = game_map.get_agent_loc(agent.id)
            if loc.state.orbs > 0:
                print('found orbs!')
                controller.consume(agent.id)

if __name__ == '__main__':

    
    game = battlegame.BattleGame([example_ai, example_ai, example_ai], 5, 0.2, 0.3, 3, map_seed=1, max_turns=100)
    print(game.pool.get_info())
    #for aid, agent in game.pool.get_info().items():
    #    print(type(aid))
    #exit()
    i = 1
    while not game.is_finished:
        print(f'Starting turn {i}.')
        game.step()
        i += 1
        if i > game.max_turns:
            break

        # print some data about the results
        agent_levels = dict()
        agent_health = dict()
        for agent in game.pool.values():
            agent_levels.setdefault(agent.team_id, [])
            agent_levels[agent.team_id].append(agent.level)
            
            agent_health.setdefault(agent.team_id, [])
            agent_health[agent.team_id].append(agent.health)
        
        #print(agent_health)
        #print(agent_levels)
        #print('==========================')
        #print(len(game.pool.agents))
        #from functools import reduce
        #print(reduce(lambda s1, s2: s1 | s2, [loc.agents for loc in game.map.locations]))
        #print(game.map.get_agent_loc(0))
    game.save_game_state('tmp/save_game1.json')
