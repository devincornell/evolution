import random
import collections

import battlegame
import mase
from mase import agentstatepool

def example_ai(team_id: int, game_map: mase.HexMap, pool: mase.AgentStatePool, controller: battlegame.BattleController):
    #print(f'Starting team {team_id} turn!')
    for agent in pool.agents():
        loc = game_map.get_agent_loc(agent.id)
        if loc.state.orbs > 0:
            print('found orbs!')
            controller.consume(agent.id)

if __name__ == '__main__':

    
    game = battlegame.BattleGame([example_ai, example_ai, example_ai], 10, 0.2, 0.9, 10, 100)
    
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
        
        print(agent_health)
        print(agent_levels)
        print('==========================')
