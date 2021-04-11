from src.simulator.element import Element
from src.simulator.reservoir import Reservoir

class Source(Element):
    def __init__(self, destination=None):
        assert destination is not None, "You have specify the destination of the Source using the keyword argument 'destination'"
        assert type(destination) is Reservoir, "'destination' must be a Reservoir"
    
        self.system = destination.system
        self.destination = destination

        self.system.add_source(self)
    

class ConstantSource(Source):
    def __init__(self, destination=None, flow=None):
        super(ConstantSource, self).__init__(destination)
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