import random
import numpy as np

from src.simulator.element import Element
from src.simulator.reservoir import Reservoir

class Demand(Element):
    def __init__(self, source=None):
        assert source is not None, "You have specify the source of the Demand using the keyword argument 'source'"
        assert isinstance(source, Reservoir), "'source' must be a Reservoir"
    
        self.system = source.system
        self.source = source

        self.system.add_demand(self)
    

class RandomDemand(Demand):
    def __init__(self, source=None, seed=42, range=None):
        super(RandomDemand, self).__init__(source)
        assert range is not None, "A range is required by a RandomDemand"

        self.source = source
        self.range = range
        self.seed = seed

        self.reset()
    
    def reset(self):
        self.rng = random.Random(self.seed)
    
    def step(self, t, dt):
        quantity = self.rng.randrange(*self.range)
        self.source.decrease(quantity)

        return {
            "quantity": quantity
        }


class GaussianDemand(Demand):
    def __init__(self, scale, mu, std, period, source=None, seed=42, bins=None, samples=1000):
        super(GaussianDemand, self).__init__(source)

        self.source = source
        self.seed = seed

        self.scale = scale
        self.mu = mu
        self.std = std
        self.period = period
        self.bins = period if bins is None else bins
        self.samples = samples

        self.init()
    
    def init(self):
        self.rng = np.random.default_rng(seed=self.seed)
        gaussian_noise = self.rng.normal(self.mu, self.std, self.samples)
        self.hist, edges = np.histogram(gaussian_noise, self.bins, density=True)
        self.hist *= self.scale
    
    def reset(self):
        pass

    def step(self, t, dt):
        quantity = self.hist[t % self.period]
        self.source.decrease(quantity)

        return {
            "quantity": quantity
        }
    


class LoopbackGaussianDemand(GaussianDemand):
    def __init__(self, scale, mu, std, period, destination, source=None, seed=42, bins=None, samples=1000):
        super(LoopbackGaussianDemand, self).__init__(scale, mu, std, period, source, seed, bins, samples)
        assert isinstance(destination, Reservoir), "'destination' must be a Reservoir"
        
        self.destination = destination

    def step(self, t, dt):
        stats = super(LoopbackGaussianDemand, self).step(t, dt)
        self.destination.increase(stats["quantity"])
        return stats
        


class StaticDemand(Demand):
    def __init__(self, source, demand):
        super(StaticDemand, self).__init__(source)
        assert isinstance(demand, list), "'demand' must be a list"
        self.demand = demand

    def reset(self):
        self.index = 0
    
    def step(self, t, dt):
        #TODO interpolation
        quantity = self.demand[t % len(self.demand)]
        self.source.decrease(quantity)

        return {
            "quantity": quantity
        }


class LoopbackStaticDemand(StaticDemand):
    def __init__(self, source, destination, demand):
        super(LoopbackStaticDemand, self).__init__(source, demand)
        assert isinstance(destination, Reservoir), "'destination' must be a Reservoir"
        
        self.destination = destination

    def step(self, t, dt):
        stats = super(LoopbackStaticDemand, self).step(t, dt)
        self.destination.increase(stats["quantity"])
        return stats
        
