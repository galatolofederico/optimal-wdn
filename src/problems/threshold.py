import numpy as np

from src.problems.wds import WaterDemandProblem
from src.runner import ThresholdRunner

class WaterDemandThresholdProblem(WaterDemandProblem):
    def __init__(self):
        super(WaterDemandThresholdProblem, self).__init__()

        self.runner = ThresholdRunner(self.wds, reservoirs=[self.r1, self.r2], on_thresholds=[10, 10], off_thresholds=[5, 5])

        super(WaterDemandProblem, self).__init__(
                    n_var=4,
                    n_obj=3,
                    n_constr=1,
                    xl=np.zeros(4),
                    xu=np.ones(4)*20
                )

    def export_X(self, X):
        p1_on, p2_on, p1_off, p2_off = X

        return dict(
            pump1_on=p1_on,
            pump1_off = p1_off,
            pump2_on=p2_on,
            pump2_off=p2_off
        )