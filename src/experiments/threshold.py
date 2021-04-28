import numpy as np

from src.problems import *
from src.runners import *
from src.simulator import *

from src import Logger, Fitness, ResultsProcessor
from src.experiments.prototype import PrototypeExperiment
from src.experiments.casestudy import CaseStudyExperiment

class ThresholdPrototypeExperiment(PrototypeExperiment):
    def __init__(self):
        super(ThresholdPrototypeExperiment, self).__init__()

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




class ThresholdCaseStudyExperiment(CaseStudyExperiment):
    def __init__(self):
        super(ThresholdCaseStudyExperiment, self).__init__()

        self.problem = WaterDemandProblem(
            evaluation_period = 24,
            problem_arguments=dict(
                n_var=len(self.pumps)*2,
                n_obj=3,
                n_constr=1,
                xl=np.zeros(len(self.pumps)*2),
                xu=np.ones(len(self.pumps)*2)*50
            ),
        )

        self.init_runner()
        self.init_fitness()
    
    def init_fitness(self):
        self.problem.set_fitness(
            self.fitness,
            fitness_args = dict(
                reservoirs=[self.tank],
                pumps=self.pumps
            ),
            feasible_args = dict(
                reservoirs=[self.tank] + self.reservoirs
            )
        )
    
    def init_runner(self):
        self.runner = ThresholdRunner(self.wds)
        self.problem.set_runner(self.runner)

