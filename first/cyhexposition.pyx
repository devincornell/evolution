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
        return self.q# + (self.r + (self.r & 1))/2

    @property
    def y(self):
        return self.r + (self.q + (self.q&1)) / 2

    def as_tuple(self):
        return (self.q, self.r, self.s)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        #return f'{self.__class__.__name__}({self.q}, {self.r}, {self.s})'
        return f'{self.as_tuple()}'

    def dist(self, other):
        return self.cy_dist(other)
    
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


    def shortest_path_dfs(self, target, avoidset: set = None, max_dist: int = None, verbose: bool = False):
        '''Find shortest path using DFS.'''
        if max_dist is None:
            max_dist = 1e9 # real big
        
        if self.cy_dist(target) > max_dist:
            raise ValueError(f'Target {self}->{target} (dist={self.cy_dist(target)}) is outside maximum distance of {max_dist}.')

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
                elif neighbor not in avoidset and neighbor not in visited and self.cy_dist(neighbor) <= max_dist:
                    current_path.append(neighbor)
                    visited.add(neighbor)
                    found_next = True
                    break
            
            # if none of these options are valid
            if not finished and not found_next:
                if verbose: print(f'reached dead end at {current_path[-1]}.')
                visited.add(neighbor)
                current_path.pop()

            if not len(current_path):
                return None

            if verbose: print('--------------------------------\n')
            
        return current_path

    #def shortest_path_bfs(self, target, avoidset: set = None, step_size: int = 3):
    #    '''Shortest path by expanding search in stages.'''
    #    visited = set([self])
    #    fringe = self.get_fringe(visited)
    #    if target in fringe:
    #        return target
    
    cdef set get_fringe(self, set others, dist: int = 1):
        '''Get positions on the fringe of the provided nodes.'''
        fringe = set()
        for pos in others:
            fringe |= pos.neighbors(1)
        return fringe - others