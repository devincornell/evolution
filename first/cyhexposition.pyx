#import itertools
import math
#import dataclasses


#from libc.math cimport sin

import time

cdef class CHPos:
    # implemented mostly using this blog
    # https://www.redblobgames.com/grids/hexagons/#neighbors
    cdef int q
    cdef int r
    cdef int s
    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s


#@dataclasses.dataclass
cdef class CyHexPosition:
    # implemented mostly using this blog
    # https://www.redblobgames.com/grids/hexagons/#neighbors
    
    # these are not available to python
    cdef int q
    cdef int r
    cdef int s

    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    @property
    def x(self):
        return self.q + (self.r + (self.r & 1))/2

    @property
    def y(self):
        return self.r

    def as_tuple(self):
        return (self.q, self.r, self.s)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        #return f'{self.__class__.__name__}({self.q}, {self.r}, {self.s})'
        return f'{self.as_tuple()}'
    
    cpdef float cy_dist(self, CyHexPosition other):
        '''Definition of distance metric for cube coordinates.'''
        return (math.fabs(self.q-other.q) + math.fabs(self.r-other.r) + math.fabs(self.s-other.s))/2

    def get_offset(self, offset_q: int, offset_r: int, offset_s: int):
        '''Get a new object with the specified offset coordinates.'''
        return self.__class__(self.q+offset_q, self.r+offset_r, self.s+offset_s)

    def neighbors(self, dist: int = 1) -> set:
        '''Get neighborhood within a given distance.'''
        cdef int q, r, s
        positions = set()
        for q in range(-dist, dist+1):
            for r in range(max(-dist, -q-dist), 1+min(dist, -q+dist)):
                s = -q - r
                if not (q == 0 and r == 0):
                    positions.add(self.get_offset(q,r,s))
        return positions

    def sorted_neighbors(self, target, dist: int = 1):
        '''Return direct neighbors sorted by distance from target.'''
        return sorted(self.neighbors(dist), key=lambda n: target.cy_dist(n))


    def shortest_path_dfs(self, target, avoidset: set = None, verbose: bool = False):
        '''Find shortest path using DFS.'''
        #avoidset = avoidset.copy() # make a new copy of the avoidset
        avoidset = set(avoidset)
        visited = set([self])
        current_path: List[CyHexPosition] = [self]

        finished = False
        while not finished:
            if verbose: print(f'status: {current_path}, {visited}')
            if verbose: time.sleep(5)
            found_next = False
            for neighbor in current_path[-1].sorted_neighbors(target):
                if neighbor == target:
                    if verbose: print(f'found target {target}.')
                    current_path.append(neighbor)
                    found_next = True
                    finished = True
                    break
                    #return current_path + [neighbor]
                elif neighbor not in avoidset and neighbor not in visited:
                    current_path.append(neighbor)
                    visited.add(neighbor)
                    found_next = True
                    break
            
            # if none of these options are valid
            if not finished and not found_next:
                if verbose: print(f'reached dead end at {current_path[-1]}.')
                visited.add(neighbor)
                current_path.pop()

            if verbose: print('--------------------------------\n')
            
        return current_path


        step_iter = range(max_steps) if max_steps is not None else range()
        for i in step_iter:
            for neighbor in sorted(self.neighbors(1), key=lambda n: self.cy_dist(n)):
                if neighbor == target:
                    return [neighbor]
                elif neighbor not in avoidsets[i]:
                    current_path.append(neighbor)

    def shortest_path_recusrsive(self, target, avoidset: set = None, max_steps: int = None):
        if avoidset is None:
            avoidset = set()
        visited = set([self])
        shortest_path = list()

        for neighbor in sorted(self.neighbors(1), key=lambda n: self.cy_dist(n)):
            if neighbor == target:
                return [neighbor]
            else:
                num_steps = max_steps-1 if max_steps is not None else None
                shortest_path += neighbor.pathfind(target, avoidset | visited, num_steps)
        

        

    def pathfind3(self, target, avoidset: set, steps: int):
        '''Find shortest path between this position and the target, avoiding avoidset.'''
        # https://www.redblobgames.com/grids/hexagons/#range
        visited = set([self])
        paths = {0: [self]}

        for i in range(steps):
            paths[i+1] = []
            for pos in paths[i]:
                for neighbor in pos.neighbors(1):
                    if neighbor not in avoidset and neighbor not in visited:
                        visited.add(neighbor)
        return visited

