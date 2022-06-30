import dataclasses
from re import X
import typing
import numpy as np
import itertools

#from first.agentid import AgentID
from .agentstate import AgentState, AgentID

from .location import Location
from .cyhexposition import CyHexPosition


class HexGrid:
    locs: typing.Dict[CyHexPosition, Location] = dict()

    def __init__(self, size: int):
        self.size = size
        
        radius = self.size // 2
        rng = list(range(-radius, radius + 1))
        
        #self.loc[ for q,r,s in itertools.product(rng, rng, rng)
        
        

    