from src.simulator.element import ActiveElement
from src.simulator.reservoir import Reservoir

class Pump(ActiveElement):
    def __init__(self, source=None, destination=None, flow=None, power=1, name=None):
        super(Pump, self).__init__(name)
        assert source is not None, "You have specify a reservoir source of the Pump using the keyword argument 'source'"
        assert destination is not None, "You have specify a destination of the Pump using the keyword argument 'destination'"
        
        assert type(source) is Reservoir, "'source' must be a Reservoir"
        assert type(destination) is Reservoir, "'destination' must be a Reservoir"

        assert source.system == destination.system, "'source' and 'destination' must be in the same System"

        assert flow is not None, "You have to specify the pump flow"

        self.system = source.system
        self.flow = flow
        self.source = source
        self.destination = destination
        self.power = power

        self.system.add_pump(self)
    
    def reset(self):
        pass

    def step(self, action, t, dt):
        quantity = 0
        
        if action == 1:
            quantity = self.flow * dt

            self.source.decrease(quantity)
            self.destination.increase(quantity)
        
        return {
            "quantity": quantity
        }