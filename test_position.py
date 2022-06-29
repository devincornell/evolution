
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
        print(len(neighbors), expected_neighbors, [6*(j+1) for j in range(i)])
        assert(len(neighbors) == expected_neighbors)

        # check that they do not exceed expected distance
        assert(all(center.dist(h)<=i for h in neighbors))

if __name__ == '__main__':
    test_neighbors()

