import numpy as np

from src.problems import *
from src.runners import *
from src.simulator import *

from src import Logger, Fitness, ResultsProcessor



class ThresholdPrototype:
    def __init__(self):
        self.problem = WaterDemandProblem(
            evaluation_period = 24,
            problem_arguments=dict(
                n_var=4,
                n_obj=3,
                n_constr=1,
                xl=np.zeros(4),
                xu=np.ones(4)*20
            ),
        )

        self.init_system()
        self.init_runner()
        self.init_fitness()
    
    def init_fitness(self):
        self.problem.set_fitness(
            self.fitness,
            fitness_args = dict(
                reservoirs=[self.tank],
                pumps=[self.p1, self.p2]
            ),
            feasible_args = dict(
                reservoirs=[self.tank, self.r1, self.r2]
            )
        )
    
    def init_runner(self):
        self.runner = ThresholdRunner(self.wds)
        self.problem.set_runner(self.runner)


    def init_system(self):
        self.d1_demand = [1.32, 1.32, 0.936, 0.936, 0.936, 2.352, 2.352, 2.352, 2.352, 0.936, 0.936, 1.32, 1.32, 1.32, 1.32, 1.32, 0.402, 0.402, 0.402, 0.402, 0.402, 0.402, 0.402, 0.402]
        self.d2_demand = [0.924, 0.924, 2.01, 2.01, 2.01, 2.454, 2.454, 2.454, 2.454, 1.44, 1.44, 2.01, 2.01, 2.01, 2.01, 2.01, 0.414, 0.414, 0.414, 0.414, 0.414, 0.414, 0.414, 0.414]

        self.wds = System(dt=1)

        self.tank = Reservoir(system=self.wds, max_volume=30, min_volume=10, initial_volume=30)
        self.r1 = Reservoir(system=self.wds, max_volume=14, min_volume=4, initial_volume=4)
        self.r2 = Reservoir(system=self.wds, max_volume=14, min_volume=4, initial_volume=4)

        self.p1 = Pump(source=self.r1, destination=self.tank, flow=3, power=8)
        self.p2 = Pump(source=self.r2, destination=self.tank, flow=3, power=8)

        self.d1 = LoopbackStaticDemand(demand=self.d1_demand, source=self.tank, destination=self.r1)
        self.d2 = LoopbackStaticDemand(demand=self.d2_demand, source=self.tank, destination=self.r2)

        self.logger = Logger(groups={
            "reservoirs": [self.tank, self.r1, self.r2],
            "pumps": [self.p1, self.p2],
            "demands": [self.d1, self.d2],
        })

        self.wds.add_logger(self.logger)
        self.fitness = Fitness(self.logger)
