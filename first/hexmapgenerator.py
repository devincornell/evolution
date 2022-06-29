
import random

from .hexmap import HexMap

def random_map(map_size: int, seed: int = 0):
    hmap = HexMap(map_size)
    
    all_positions = hmap.positions()
    
    # random sampling for start, end, and blocks
    random.seed(seed)
    avoidset = set(random.sample(all_positions, len(all_positions) // 4))
    start = random.choice(list(all_positions))
    end = start
    while end == start:
        end = random.choice(list(all_positions))
    
    path = start.shortest_path_dfs(end, avoidset, 2*map_size)
    
    return start, end, avoidset

def run_test(map_size: int, num_runs: int):
    hmap = HexMap(map_size)
    path_lengths = list()
    for i in range(num_runs):
        start, end, avoidset = test_data(hmap, i)
        path = start.shortest_path_dfs(end, avoidset, 2*map_size)
        path_lengths.append(len(path))
    return start, end, sum(pl for pl in path_lengths if pl is not None)








