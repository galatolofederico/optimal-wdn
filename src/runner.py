import numpy as np
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


class ThresholdRunner(Runner):
    def __init__(self, system, reservoirs, on_thresholds, off_thresholds):
        super(ThresholdRunner, self).__init__(system)

        self.reservoirs = reservoirs
        self.on_thresholds = on_thresholds
        self.off_thresholds = off_thresholds

    def get_parameters(self):
        return self.on_thresholds + self.off_thresholds
    
    def set_parameters(self, parameters):
        self.on_thresholds = parameters[:2]
        self.off_thresholds = parameters[2:]
    
    def run(self, steps):
        self.system.reset()
        actions = [0, 0]
        for i in range(0, steps):
            for i, (on_threshold, off_threshold, reservoir) in enumerate(zip(self.on_thresholds, self.off_thresholds, self.reservoirs)):
                action = None
                if reservoir.current_volume < off_threshold:
                    actions[i] = 0
                if reservoir.current_volume > on_threshold:
                    actions[i] = 1
            
            self.system.step(actions)



class SequenceRunner(Runner):
    def __init__(self, system, pumps=2, length=24):
        super(SequenceRunner, self).__init__(system)
        self.pumps = pumps
        self.length = length

        self.sequence = np.ones((self.length, self.pumps))

    def get_parameters(self):
        return self.sequence
    
    def set_parameters(self, sequence):
        self.sequence = sequence.reshape((self.length, self.pumps)) > 0.5
    
    def run(self, steps):
        self.system.reset()
        for i in range(0, steps):
            actions = self.sequence[i % self.sequence.shape[0]]
            self.system.step(actions)
