
import dataclasses


import dataclasses

@dataclasses.dataclass
class v1ProtoConfig:
    
    
    def evaluate(self, game_map):
        agents = game_map.agents()
        
        

class v1ProtoAI:
    '''The boss of all AIs.'''
    def __init__(self, config: v1ProtoConfig):
        self.config = config







