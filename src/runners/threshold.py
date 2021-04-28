import numpy as np

from src.runners.runner import Runner

class ThresholdRunner(Runner):
    def __init__(self, system):
        super(ThresholdRunner, self).__init__(system)

        self.reservoirs = list()
        self.on_thresholds = list()
        self.off_thresholds = list()

        for pump in self.system.pumps:
            self.reservoirs.append(pump.source)
            self.on_thresholds.append(float(pump.source.max_volume)-1)
            self.off_thresholds.append(float(pump.source.min_volume)+1)

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

    def export_X(self, X):
        p1_on, p2_on, p1_off, p2_off = X

        return dict(
            pump1_on=p1_on,
            pump1_off = p1_off,
            pump2_on=p2_on,
            pump2_off=p2_off
        )