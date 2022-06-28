import numpy as np
import first
import random

if __name__ == '__main__':
    #mm = first.ModelMap(10, 5)
    p = first.CyHexPosition(0, 0, 0)

    radius = 5000
    for n in p.neighbors(radius):
        assert(p.cy_dist(n) <= radius)

    exit()


    avoidset = set([
        first.CyHexPosition(-1, 1, 0),
        first.CyHexPosition(-2, 2, 0),
        first.CyHexPosition(-3, 3, 0),
        first.CyHexPosition(-2, 3, -1),
        first.CyHexPosition(-1, 3, -2),
        first.CyHexPosition(-2, 0, 2),
        first.CyHexPosition(-1, -1, 2),
        first.CyHexPosition(3, -1, -2),
    ])

    target = first.CyHexPosition(-3, 4, -1)

    path = p.shortest_path_dfs(target, avoidset)
    pathset = set(path)
    print(path)

    hmap = first.HexMap(5, {'blocked': False, 'passed': True})
    positions = hmap.positions()
    
    for loc in hmap:
        loc.state['blocked'] = loc.pos in avoidset
        loc.state['passed'] = loc.pos in pathset

    loc_info = hmap.get_loc_info()
    for ldata in loc_info:
        print(ldata)

    import pickle
    with open('tmp/tmp_loc_info.pic', 'wb') as f:
        pickle.dump(loc_info, f)

    exit()
    for r in p.neighbors():
        print(r)
        
    path = p.pathfind(first.CyHexPosition(-1, 0, 1), set(), 5)
    print(path)
    #center = first.Position(0,0)
    
    #print(mm.locs)
    #print(mm[center])
    #print(mm.region(center, 1))
    
    #a = np.array([[1, 2, 3],[4, 5, 6],[7,8,9]])
    #print(a[-1:2, 0:2])





