import dataclasses
from re import X
import typing
import numpy as np
import itertools

#from first.agentid import AgentID
from .agent import Agent, AgentID

from .location import Location
from .position import Position


class HexGrid:
    locs: typing.Dict[Position, Location] = dict()

    def __init__(self, size: int):
        self.size = size
        
        radius = self.size // 2
        rng = list(range(-radius, radius + 1))
        
        #self.loc[ for q,r,s in itertools.product(rng, rng, rng)
        
        

    