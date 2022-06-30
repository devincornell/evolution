
import mase

class BaseAgent:
    pass


class BattleGame:
    def __init__(self, map_radius: int, AgentType1: BaseAgent, AgentType2: BaseAgent):
        self.pool = mase.AgentPool()
        self.map = mase.HexMap(map_radius)
        self.agent1_type = AgentType1
        self.agent2_type = AgentType2
        
    def setup(self):
        '''Set up actual game.'''
        pass
        
    def run(self):
        '''Start the simulation.'''
        while not self.is_finished:
            self.step()
        
    @property
    def is_finished(self):
        
        
    def step(self):
        pass
    

if __name__ == '__main__':
    
    class BattleAgent1(BaseAgent):
        pass

    class BattleAgent2(BaseAgent):
        pass
    
    game = BattleGame(BattleAgent1, BattleAgent2)

    game.step()


