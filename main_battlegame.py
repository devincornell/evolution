import battlegame
import mase
import collections
#from mase.position.pyhexposition import HexPos

def run_game(seed: int = 0, save_game: bool = True):
    game = battlegame.BattleGame(
        ai_players = [battlegame.attack_consume, battlegame.consume_attack],
        map_radius = 10,
        blocked_ratio = 0.2,
        orb_ratio = 0.1,
        num_start_warriors = 10,
        map_seed=seed, 
        max_turns=50,
    )
    
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
    
    if not timeout_finish:
        #winct[game.get_winner().__name__] += 1
        return game.get_winner().__name__
    else:
        return None



if __name__ == '__main__':
    
    hexmap = mase.HexMap(10)
    print(hexmap)
    sp = hexmap.pathfind_dfs(mase.HexPos(0,0,0), mase.HexPos(-3, 3, 0))
    print(sp)
    
    import tqdm
    
    results = list()
    for seed in tqdm.tqdm(range(500)):
        result = run_game(seed)
        results.append(result)
        winct = collections.Counter(results)
        print('\n', winct)
    
    exit()
    seeds = list(range(100))
    
    import multiprocessing
    with multiprocessing.Pool(10) as p:
        results = p.map(run_game, seeds)

        
    #print(collections.Counter(results))
    