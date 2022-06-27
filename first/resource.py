
import dataclasses


@dataclasses.dataclass
class Resource:
    __slots__ = ['amnt']
    amnt: int
