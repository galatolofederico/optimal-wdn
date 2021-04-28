import numpy as np
from src.logger import Logger

class Fitness:
    def __init__(self, logger, energy_price=1):
        assert isinstance(logger, Logger), "a Logger is needed to compute the fitness"
        self.logger = logger
        self.energy_price = energy_price
    
    def fitness(self, reservoirs, pumps):
        switches = 0
        energy = 0
        for pump in pumps:
            history = self.logger.get_object_history(pump)

            y = np.array([i["value"] for i in history["quantity"]])
            y = (y > 0).astype(int)
            
            changes = np.where(np.diff(y))[0]

            switches += len(changes)
            energy += y.sum()*pump.power
        
        energy *= self.energy_price

        volume_deltas = 0
        for reservoir in reservoirs:
            history = self.logger.get_object_history(reservoir)

            y = np.array([i["value"] for i in history["current_volume"]])

            volume_deltas += np.abs(reservoir.initial_volume - y[-1])
        
        return {
            "energy": energy,
            "switches": switches,
            "volume_deltas": volume_deltas
        }

    def feasible(self, reservoirs):
        underflow = 0.0
        for reservoir in reservoirs:
            history = self.logger.get_object_history(reservoir)
            y = np.array([i["value"] for i in history["underflow_volume"]])
            underflow += y[-1]
        
        return {
            "underflow": underflow
        }