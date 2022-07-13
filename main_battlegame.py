import battlegame
import exampleai
import mase
from mase.position.pyhexposition import HexPos

def run_game(seed):
    game = battlegame.BattleGame(
        ai_players = [exampleai.consume_attack, exampleai.attack_consume],
        map_radius = 8,
        blocked_ratio = 0.2,
        food_ratio = 0.01,
        num_start_warriors = 3,
        map_seed=seed, 
        max_turns=500,
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
    
    hexmap = mase.HexNetMap(10)
    print(hexmap)
    print(len(hexmap.graph.es))
    hexmap.graph.write_graphml('tmp/mynet.graphml')
    sp = hexmap.shortest_path(HexPos(0,0,0), HexPos(-2,1,1))
    print(sp)
    exit()
    
    import tqdm
    save_game = True
    winct = collections.Counter()
    #for seed in tqdm.tqdm(range(100)):
    seeds = list(range(100))
    
    import multiprocessing
    with multiprocessing.Pool(10) as p:
        results = p.map(run_game, seeds)

        
    print(collections.Counter(results))
    