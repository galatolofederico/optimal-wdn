import numpy as np
from pymoo.factory import get_crossover, get_mutation, get_sampling

from src.problems import WaterDemandProblem
from src.runners import ThresholdRunner, SequenceRunner
from src.experiments.prototype import get_prototype


configs = dict(
    prototype_th = dict(
        problem = dict(
            type = WaterDemandProblem,
            args = dict(
                evaluation_period = 24,
                problem_arguments=dict(
                    n_var=4,
                    n_obj=3,
                    n_constr=1,
                    xl=np.zeros(4),
                    xu=np.ones(4)*20
                ),
            ),
        ),
        runner = dict(
            type = ThresholdRunner,
            args = dict()
        ),
        experiment = dict(
            type = get_prototype,
            args = dict()
        )
    ),

    prototype_seq = dict(
        problem = dict(
            type = WaterDemandProblem,
            args = dict(
                evaluation_period = 24,
                algorithm_arguments = dict(
                    nsga2 = dict(
                        sampling=get_sampling("bin_random"),
                        crossover=get_crossover("bin_hux"),
                        mutation=get_mutation("bin_bitflip"),
                    ),
                ),
                problem_arguments=dict(
                    n_var=24*2,
                    n_obj=3,
                    n_constr=1,
                    xl=0,
                    xu=1,
                    type_var=np.bool
                ),
            ),
        ),
        runner = dict(
            type = SequenceRunner,
            args = dict()
        ),
        system = dict(
            type = get_prototype,
            args = dict()
        )
    )
)