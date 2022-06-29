import dataclasses
import math
import typing


@dataclasses.dataclass
class Position:
    __slots__ = ['x', 'y']
    x: int
    y: int

    def __hash__(self):
        return (self.x, self.y)

    def __eq__(self):
        return self.__hash__()

    def offset(self, offset_x: int, offset_y: int):
        return Position(self.x+offset_x, self.y+offset_y)

    def dist(self, other):
        return math.sqrt((self.x-other.x)** + (self.y-other.y)**2)

