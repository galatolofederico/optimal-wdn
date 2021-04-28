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
        assert len(parameters) % 2 == 0
        self.on_thresholds = parameters[:len(parameters)//2]
        self.off_thresholds = parameters[len(parameters)//2:]
    
    def run(self, steps):
        self.system.reset()
        actions = np.zeros((len(self.reservoirs)))
        for i in range(0, steps):
            for i, (on_threshold, off_threshold, reservoir) in enumerate(zip(self.on_thresholds, self.off_thresholds, self.reservoirs)):
                action = None
                if reservoir.current_volume < off_threshold:
                    actions[i] = 0
                if reservoir.current_volume > on_threshold:
                    actions[i] = 1
            
            self.system.step(actions)

    def export_X(self, X):
        assert len(X) % 2 == 0
        on_thresholds = X[:len(X)//2]
        off_thresholds = X[len(X)//2:]
        
        ret = dict()

        for i, (on_threshold, off_threshold) in enumerate(zip(on_thresholds, off_thresholds)):
            ret[f"pump{i}_on"]  = on_threshold
            ret[f"pump{i}_off"] = off_threshold

        return ret