import battlegame
import mase
import collections
#from mase.position.pyhexposition import HexPos

def run_game(seed: int = 0, save_game: bool = True):
    game = battlegame.BattleGame(
        ai_players = [battlegame.attack_consume_ai, battlegame.consume_attack_ai, battlegame.random_walk_ai],
        map_radius = 10,
        blocked_ratio = 0.2,
        orb_ratio = 0.1,
        num_start_warriors = 10,
        map_seed=seed, 
        max_turns=100,
        verbose = False,
    )
    
    # test out a*
    #agents = list(game.map.agents())
    #use_pos = [loc.pos for loc in game.map.locations() if not loc.num_agents and not loc.state.is_blocked]
    #print(agents[0].shortest_path(agents[1].pos, use_pos, verbose=False))
    #
    #game.save_game_state(f'tmp/ASTAR_TEST.json')
    #exit()
    
    timeout_finish = False
    i = 1
    while not game.is_finished():
        game.step()
        i += 1
        if i > game.max_turns:
            timeout_finish = True
            break
    
    if save_game:
        game.save_game_state(f'tmp/save_game_{seed}.json')
    
    winner = game.get_winner().__name__ if not timeout_finish else None
    print(f'finished {seed}. Winner: {winner}')
    return winner



if __name__ == '__main__':
    
    hexmap = mase.HexMap(10)
    print(hexmap)
    #sp = hexmap.pathfind_dfs(mase.HexPos(0,0,0), mase.HexPos(-3, 3, 0))
    #print(sp)
    
    import tqdm
    
    #print(run_game(497))
    #exit()
    
    if False:
        results = list()
        for seed in tqdm.tqdm(range(500)):
            result = run_game(seed)
            results.append(result)
            winct = collections.Counter(results)
            print('\n', winct)
    else:
        import multiprocessing
        seeds = list(range(500))
        with multiprocessing.Pool(24) as p:
            results = p.map(run_game, seeds)

    print(collections.Counter(results))
    