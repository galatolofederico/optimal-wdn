from src.simulator import System

class Runner:
    def __init__(self, system):
        self.system = system
        assert isinstance(self.system, System)
    
    def get_parameters(self):
        raise NotImplementedError
    
    def set_parameters(self, parameters):
        raise NotImplementedError
    
    def run(self, steps):
        raise NotImplementedError