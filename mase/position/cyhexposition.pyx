# distutils: language = c++

#%%cython


#import itertools
#import math
#import dataclasses
#from libcpp.set cimport set as cpp_set
#cimport libcpp.set.set

#from libc.math cimport sin

import time
from libc.math cimport abs as c_abs
from .errors import *

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

    def coords(self):
        return (self.q, self.r, self.s)

    def __eq__(self, other):
        #return self.q == other.q and self.r == other.r and self.s == other.s
        return self.coords() == other.coords()

    def __repr__(self):
        #return f'{self.__class__.__name__}({self.q}, {self.r}, {self.s})'
        return f'{self.coords()}'

    def dist(self, other):
        return self.cy_dist(other)

    def offset(self, offset_q: int, offset_r: int, offset_s: int):
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
                    positions.add(self.cy_offset(q,r,s))
        return positions

    def sorted_neighbors(self, target, dist: int = 1):
        '''Return direct neighbors sorted by distance from target.'''
        return sorted(self.neighbors(dist), key=lambda n: target.cy_dist(n))

    def pathfind_dfs(self, target, avoidset: set = None, max_dist: int = None, verbose: bool = False):
        '''Heuristic-based pathfinder. May not be shortest path.'''
        if target in avoidset:
            raise TargetInAvoidSet(f'Target {target} was found in avoidset.')
        
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

    def shortest_path_length(self, target, avoidset: set) -> int:
        '''Calculate number of steps required to reach target.'''
        if target in avoidset:
            raise TargetInAvoidSet(f'Target {target} was found in avoidset.')
        
        cdef int ct = 0
        visited = set([self])
        while True:
            fringe = self.cy_fringe(visited) - avoidset
            ct += 1
            if target in fringe:
                ct += 1
                return ct
            elif not len(fringe):
                return None
            else:
                visited |= fringe
    
    def fringe(self, others: set, dist: int = 1) -> set:
        return self.cy_fringe(others, dist)

    cdef CyHexPosition cy_offset(self, int delta_q, int delta_r, int delta_s):
        return CyHexPosition(self.q+delta_q, self.r+delta_r, self.s+delta_s)

    cpdef float cy_dist(self, CyHexPosition other):
        '''Definition of distance metric for cube coordinates.'''
        return (c_abs(self.q-other.q) + c_abs(self.r-other.r) + c_abs(self.s-other.s))/2

    cdef set cy_fringe(self, set others, int dist = 1):
        '''Get positions on the fringe of the provided nodes.'''
        others = others | set([self])
        fringe = set()
        for pos in others:
            fringe |= pos.neighbors(dist)
        return fringe - others


