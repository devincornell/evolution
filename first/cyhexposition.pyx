#import itertools
import math
#import dataclasses

#@dataclasses.dataclass
cdef class CyHexPosition:
    cdef int q
    cdef int r
    cdef int s

    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s

    def __hash__(self):
        return (self.q, self.r, self.s)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    def sum(self):
        return self.q + self.r + self.s
    
    def __sub__(self, other):
        '''Get directional vector.'''
        return self.__class__(self.q-other.q, self.r-other.r, self.s-other.s)
    
    def offset_pos(self, other):
        '''Return current position offset by interpreting other as a difference.'''
        return self.__class__(self.q+other.q, self.r+other.r, self.s+other.s)

    def offset(self, offset_q: int, offset_r: int, offset_s: int):
        return self.__class__(self.q+offset_q, self.r+offset_r, self.s+offset_s)

    def dist(self, other):
        return math.sqrt((self.x-other.x)** + (self.y-other.y)**2)

    #def neighbors(self, int dist):

    def get_offsets(self, dist: int) -> list:
        cdef int q, r, s
        positions = list()
        for q in range(-dist, dist+1):
            for r in range(max(-dist, -q-dist), 1+min(dist, -q+dist)):
                s = -q - r
                positions.append(self.offset(q,r,s))
        return positions

    #def region(self, dist: int):
    #    '''Points corresponding to the region around this point.'''
    #    rng = list(range(-dist, dist + 1))
    #    return [self.offset(q,r,s) for q,r,s in itertools.product(rng,rng,rng) if (q+r+s)==0]



