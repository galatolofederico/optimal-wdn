import numpy as np

from src.problems import *
from src.runners import *
from src.simulator import *

from src import Logger, Fitness, ResultsProcessor
from src.experiments.experiment import Experiment

class CaseStudyExperiment(Experiment):
    def __init__(self):
        super(CaseStudyExperiment, self).__init__()
        self.init_system()

    def init_system(self):
        self.wds = System(dt=1)

        self.tank = Reservoir(system=self.wds, max_volume=200, min_volume=20, initial_volume=100)

        costant_sources = 10
        normal_sources = 10

        self.reservoirs = list()
        for i in range(0, costant_sources+normal_sources):
            self.reservoirs.append(Reservoir(system=self.wds, max_volume=50, min_volume=5, initial_volume=10))

        self.sources = list()
        for i in range(0, costant_sources):
            self.sources.append(ConstantSource(destination=self.reservoirs[i], flow=0.5))
        
        for i in range(0, normal_sources):
            self.sources.append(GaussianSource(
                scale=15, mu=12, std=5, period=24, seed=i,
                destination=self.reservoirs[costant_sources + i],
            ))

        
        uniform_demands = 5
        normal_demands = 10
        double_normal_demands = 5
        
        self.demands = list()
        for i in range(0, uniform_demands):
            self.demands.append(UniformDemand(source=self.tank, range=[0.8, 1.2], seed=i))

        for i in range(0, normal_demands):
            self.demands.append(GaussianDemand(source=self.tank, mu=0, std=5, scale=20, period=24, seed=i))

        for i in range(0, double_normal_demands):
            self.demands.append(DoubleGaussianDemand(source=self.tank, mus=[6, 18], stds=[2, 2], scale=10, period=24, seed=i))

        
        self.pumps = list()
        for reservoir in self.reservoirs:
            self.pumps.append(Pump(source=reservoir, destination=self.tank, flow=1, power=1))

        
        self.logger = Logger(groups={
            "reservoirs": [self.tank] + self.reservoirs,
            "pumps": self.pumps,
            "demands": self.demands,
            "sources": self.sources
        })

        self.wds.add_logger(self.logger)
        self.fitness = Fitness(self.logger)
