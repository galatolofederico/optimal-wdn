import numpy as np
import os
from pymoo.model.problem import Problem
import json

from src.simulator import *
from src import Logger, Fitness, ResultsProcessor

class WaterDemandProblem(Problem):
    def __init__(self):
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

        self.algorithm_arguments = dict() 

        self.evaluation_period = 24
     
    def _evaluate(self, X, out, *args, **kwargs):
        values = dict()
        for parameters in X:
            self.runner.set_parameters(parameters)
            self.runner.run(self.evaluation_period)

            results = self.fitness.fitness(reservoirs=[self.tank], pumps=[self.p1, self.p2])
            constraints = self.fitness.feasible(reservoirs=[self.tank, self.r1, self.r2])

            for k, v in results.items():
                if k not in values: values[k] = list()
                values[k].append(v)
            
            if "constraints" not in values: values["constraints"] = list()
            values["constraints"].append(constraints["underflow"])
        
        f1 = np.array(values["energy"])
        f2 = np.array(values["switches"])
        f3 = np.array(values["volume_deltas"])

        g = values["constraints"]
        
        out["F"] = np.column_stack([f1, f2, f3])
        out["G"] = np.column_stack([g])

    def get_names(self):
        return dict(
            objectives=["energy", "switches", "volume_deltas"],
            constraints=["underflow"]
        )

    def export_results(self, parameters, objectives, folder):
        self.runner.set_parameters(parameters)
        self.runner.run(self.evaluation_period)

        processor = ResultsProcessor(self.logger)
        data = processor.plot({
            "reservoirs": ["current_volume", "overflow_volume"],
            "pumps": ["quantity"],
            "demands": ["quantity"],
        }, folder)

        processor.export_xslx(data, os.path.join(folder, "metrics.xlsx"))

        results = dict(
            X = self.export_X(parameters),
            F = dict(
                energy = objectives[0],
                switches = objectives[1],
                volume_deltas = objectives[2],
            )
        )

        json.dump(results, open(os.path.join(folder, "results.json"), "w"))        

        