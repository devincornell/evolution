import numpy as np
import first

if __name__ == '__main__':
    #mm = first.ModelMap(10, 5)
    p = first.HexPosition(0, 0, 0)
    print(p)
    
    for r in p.region(1):
        print(r)
    
    #center = first.Position(0,0)
    
    #print(mm.locs)
    #print(mm[center])
    #print(mm.region(center, 1))
    
    #a = np.array([[1, 2, 3],[4, 5, 6],[7,8,9]])
    #print(a[-1:2, 0:2])





