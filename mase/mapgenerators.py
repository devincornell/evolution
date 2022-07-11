import typing
import igraph

from .position import PyHexPosition

def neighbors(self, dist: int = 1) -> typing.Set[PyHexPosition]:
    '''Get neighborhood within a given distance.'''
    positions = set()
    for q in range(-dist, dist+1):
        for r in range(max(-dist, -q-dist), 1+min(dist, -q+dist)):
            s = -q - r
            if not (q == 0 and r == 0):
                positions.add(self.offset(q,r,s))
    return positions






