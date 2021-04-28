import numpy as np

from src.simulator.element import Element
from src.simulator.reservoir import Reservoir

class Source(Element):
    def __init__(self, destination=None, name=None):
        super(Source, self).__init__(name)
        assert destination is not None, "You have specify the destination of the Source using the keyword argument 'destination'"
        assert type(destination) is Reservoir, "'destination' must be a Reservoir"
    
        self.system = destination.system
        self.destination = destination

        self.system.add_source(self)
    

class ConstantSource(Source):
    def __init__(self, destination=None, flow=None, name=None):
        super(ConstantSource, self).__init__(destination, name=name)
        assert flow is not None, "You have to specify a flow for a ConstantSource"
        
        self.flow = flow

    def reset(self):
        pass

    def step(self, t, dt):
        quantity = self.flow*dt
        self.destination.increase(quantity)
        
        return {
            "quantity": quantity
        }



class GaussianSource(Source):
    def __init__(self, scale, mu, std, period, destination=None, seed=42, bins=None, samples=1000, name=None):
        super(GaussianSource, self).__init__(destination, name=name)

        self.destination = destination
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
        self.destination.increase(quantity)
        
        return {
            "quantity": quantity
        }