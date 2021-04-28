import numpy as np
from pymoo.factory import get_crossover, get_mutation, get_sampling

from src.problems import *
from src.runners import *
from src.simulator import *

from src import Logger, Fitness, ResultsProcessor
from src.experiments.prototype import PrototypeExperiment

class SequencePrototypeExperiment(PrototypeExperiment):
    def __init__(self):
        super(SequencePrototypeExperiment, self).__init__()
        self.evaluation_period = 24
        self.pumps = 2

        self.problem = WaterDemandProblem(
            evaluation_period = self.evaluation_period,
            problem_arguments=dict(
                n_var=self.evaluation_period*self.pumps,
                n_obj=3,
                n_constr=1,
                xl=0,
                xu=1,
                type_var=np.bool
            ),
        )

        self.algorithm_arguments = dict(
            nsga2=dict(
                sampling=get_sampling("bin_random"),
                crossover=get_crossover("bin_hux"),
                mutation=get_mutation("bin_bitflip"),
            )
        )


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
        self.runner = SequenceRunner(self.wds, pumps=self.pumps, length=self.evaluation_period)
        self.problem.set_runner(self.runner)

