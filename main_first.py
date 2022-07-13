import numpy as np
import first
import random

if __name__ == '__main__':
    #mm = first.ModelMap(10, 5)
    start = first.HexPos(0, 0, 0)

    avoidset = set([
        first.HexPos(-1, 1, 0),
        first.HexPos(-2, 2, 0),
        first.HexPos(-3, 3, 0),
        first.HexPos(-2, 3, -1),
        first.HexPos(-1, 3, -2),
        first.HexPos(-2, 0, 2),
        first.HexPos(-1, -1, 2),
        first.HexPos(3, -1, -2),
    ])

    target = first.HexPos(-3, 4, -1)

    path = start.shortest_path_dfs(target, avoidset)
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

    import json
    with open('tmp/example_sim.json', 'w') as f:
        json.dump(loc_info, f)

    exit()
    for r in p.neighbors():
        print(r)
        
    path = p.pathfind(first.HexPos(-1, 0, 1), set(), 5)
    print(path)
    #center = first.HexPos(0,0)
    
    #print(mm.locs)
    #print(mm[center])
    #print(mm.region(center, 1))
    
    #a = np.array([[1, 2, 3],[4, 5, 6],[7,8,9]])
    #print(a[-1:2, 0:2])





