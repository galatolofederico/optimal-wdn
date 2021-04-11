from src.simulator.reservoir import Reservoir
from src.simulator.pump import Pump
from src.simulator.source import Source
from src.simulator.demand import Demand

from src.logger import Logger

class System:
    def __init__(self, dt=1):
        self.reservoirs = []
        self.pumps = []
        self.sources = []
        self.demands = []

        self.logger = None
        
        self.dt = dt

        self.reset()
    
    def reset(self):
        for reservoir in self.reservoirs: reservoir.reset()
        for pump in self.pumps: pump.reset()
        for source in self.sources: source.reset()
        for demand in self.demands: demand.reset()

        if self.logger is not None: self.logger.reset()
        
        self.t = 0

    def step(self, actions):
        assert len(actions) == len(self.pumps)

        for action, pump in zip(actions, self.pumps):
            stats = pump.step(action, self.t, self.dt)
            if self.logger is not None: self.logger(pump, stats, self.t)

        for source in self.sources:
            stats = source.step(self.t, self.dt)
            if self.logger is not None: self.logger(source, stats, self.t)
        
        for demand_id, demand in enumerate(self.demands):
            stats = demand.step(self.t, self.dt)
            if self.logger is not None: self.logger(demand, stats, self.t)
        
        for reservoir in self.reservoirs:
            stats = reservoir.step(self.t, self.dt)
            if self.logger is not None: self.logger(reservoir, stats, self.t)
        
        self.t += 1

    def add_logger(self, logger):
        assert isinstance(logger, Logger), "Logger expected instead of %s" % (type(reservoir).__name__)
        assert self.logger is None, "A system can have only one Logger"
        self.logger = logger

    def add_reservoir(self, reservoir):
        assert isinstance(reservoir, Reservoir), "Reservoir expected instead of %s" % (type(reservoir).__name__)
        self.reservoirs.append(reservoir)
    
    def add_pump(self, pump):
        assert isinstance(pump, Pump), "Pump expected instead of %s" % (type(pump).__name__)
        self.pumps.append(pump)

    def add_source(self, source):
        assert isinstance(source, Source), "Source expected instead of %s" % (type(source).__name__)
        self.sources.append(source)
    
    def add_demand(self, demand):
        assert isinstance(demand, Demand), "Demand expected instead of %s" % (type(demand).__name__)
        self.demands.append(demand)