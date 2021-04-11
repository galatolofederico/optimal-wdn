import numpy as np
from pymoo.factory import get_crossover, get_mutation, get_sampling

from src.problems.wds import WaterDemandProblem
from src.runner import SequenceRunner

class WaterDemandSequenceProblem(WaterDemandProblem):
    def __init__(self, pumps=2, length=24):
        super(WaterDemandSequenceProblem, self).__init__()
        self.pumps = pumps
        self.length = length

        self.runner = SequenceRunner(self.wds, pumps=self.pumps, length=self.length)

        self.algorithm_arguments = dict(
            nsga2=dict(
                sampling=get_sampling("bin_random"),
                crossover=get_crossover("bin_hux"),
                mutation=get_mutation("bin_bitflip"),
            )
        )

        super(WaterDemandProblem, self).__init__(
                    n_var=self.length*self.pumps,
                    n_obj=3,
                    n_constr=1,
                    xl=0,
                    xu=1,
                    type_var=np.bool
                )
    
    def export_X(self, X):
        X = X.reshape(self.length, self.pumps)
        ret = dict()

        for i in range(0, self.pumps):
            ret["pump_%d" % (i, )] = X[:, i].astype(float).tolist()
        
        return ret