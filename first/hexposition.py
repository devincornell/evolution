import itertools
import math
import dataclasses


hex_directions = (
    (1, -1, 0), # top-right
    (1, 0, -1), # right
    (0, 1, -1), # bottom-right
    (-1, 1, 0), # bottom-left
    (-1, 0, 1), # left
    (0, -1, 1), # top-left
)

@dataclasses.dataclass
class HexPosition:
    #__slots__ = ['q', 'r', 's']
    q: int
    r: int
    s: int

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
        return HexPosition(self.q+offset_q, self.r+offset_r, self.s+offset_s)

    def dist(self, other):
        return math.sqrt((self.x-other.x)** + (self.y-other.y)**2)

    def region(self, dist: int):
        '''Points corresponding to the region around this point.'''
        rng = list(range(-dist, dist + 1))
        return [self.offset(q,r,s) for q,r,s in itertools.product(rng,rng,rng) if (q+r+s)==0]



