#import itertools
import math
#import dataclasses



#@dataclasses.dataclass
cdef class CyHexPosition:
    # implemented mostly using this blog
    # https://www.redblobgames.com/grids/hexagons/#neighbors
    cdef int q
    cdef int r
    cdef int s

    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.q}, {self.r}, {self.s})'
    
    def dist(self, other) -> float:
        '''Definition of distance metric for cube coordinates.'''
        return (math.abs(self.q-other.q) + math.abs(self.r-other.r) + math.abs(self.s-other.s))/2

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

    def shortest_path(self, target, avoidset: set = None, max_steps: int = None):
        if avoidset is None:
            avoidset = set()
        visited = set([self])
        shortest_path = list()

        for neighbor in sorted(self.neighbors(1), key=lambda n: self.dist(n)):
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

