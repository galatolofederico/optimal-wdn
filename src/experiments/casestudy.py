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

        self.tank = Reservoir(system=self.wds, max_volume=1_000, min_volume=50, initial_volume=100)

        costant_sources = 10
        normal_sources = 10

        self.reservoirs = list()
        for i in range(0, costant_sources+normal_sources):
            self.reservoirs.append(Reservoir(system=self.wds, max_volume=50, min_volume=5, initial_volume=10))

        self.sources = list()
        for i in range(0, costant_sources):
            self.sources.append(ConstantSource(destination=self.reservoirs[i], flow=1))
        
        for i in range(0, normal_sources):
            self.sources.append(GaussianSource(
                scale=1, mu=12, std=3, period=24,
                destination=self.reservoirs[costant_sources + i],
            ))

        
        uniform_demands = 5
        normal_demands = 10
        double_normal_demands = 5
        
        self.demands = list()
        for i in range(0, uniform_demands):
            self.demands.append(UniformDemand(source=self.tank, range=[1.5, 2.5]))

        for i in range(0, normal_demands):
            self.demands.append(GaussianDemand(source=self.tank, mu=12, std=5, scale=1, period=24))

        for i in range(0, double_normal_demands):
            self.demands.append(DoubleGaussianDemand(source=self.tank, mus=[6, 18], stds=[2, 2], scales=[1, 1], period=24))

        
        self.pumps = list()
        for reservoir in self.reservoirs:
            self.pumps.append(Pump(source=reservoir, destination=self.tank, flow=2, power=1))

        
        self.logger = Logger(groups={
            "reservoirs": [self.tank] + self.reservoirs,
            "pumps": self.pumps,
            "demands": self.demands,
            "sources": self.sources
        })

        self.wds.add_logger(self.logger)
        self.fitness = Fitness(self.logger)
