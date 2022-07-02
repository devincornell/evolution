#from .numpymodelmap import *
from .location import Location, LocationState
from .hexmap import HexMap

#from .pyhexposition import PyHexPosition
#from .hexposition import HexPosition
from .hexmapgenerator import *
from .agentstatepool import AgentStatePool, AgentState, AgentID

#from .agentstate import AgentState, AgentID
from .position import HexPosition, PyHexPosition

# try to import position, but don't import if it isn't compiled
try:
    from .position import CyHexPosition
except ImportError:
    pass


