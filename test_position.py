
import sys
sys.path.append('..')
import mase

import random


def test_neighbors():
    center = mase.CyHexPosition(0, 0, 0)

    # check correct number of neighbors
    for i in range(50):
        neighbors = center.neighbors(i)
        
        # check if there is correct number
        expected_neighbors = sum([6*(j+1) for j in range(i)])
        #print(len(neighbors), expected_neighbors, [6*(j+1) for j in range(i)])
        assert(len(neighbors) == expected_neighbors)

        # check that they do not exceed expected distance
        assert(all(center.dist(h)<=i for h in neighbors))


def test_pathfind():
    for map_size in range(2, 30):
        for _ in range(20):
            start, target, avoidset = mase.hexmapgenerator.random_target_map(map_size)
            sp_len = start.shortest_path_length(target, avoidset)
            found_path = start.pathfind_dfs(target, avoidset)
            assert(len(found_path) >= sp_len)
            #print(len(found_path) - sp_len)

    

if __name__ == '__main__':
    test_neighbors()
    test_pathfind()
