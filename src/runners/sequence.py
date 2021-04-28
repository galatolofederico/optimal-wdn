import numpy as np

from src.runners.runner import Runner


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
