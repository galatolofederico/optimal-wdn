import numpy as np
import os
from pymoo.model.problem import Problem
import json

from src.runners import Runner
from src.fitness import Fitness
from src import  ResultsProcessor, Logger

class WaterDemandProblem(Problem):
    def __init__(self, problem_arguments=dict(), fitness_args=dict(), feasible_args=dict(), evaluation_period=24):
        self.problem_arguments = problem_arguments
        self.evaluation_period = evaluation_period
        self.fitness_args = fitness_args
        self.feasible_args = feasible_args

        super(WaterDemandProblem, self).__init__(**self.problem_arguments)
     
    def set_runner(self, runner):
        assert isinstance(runner, Runner)
        self.runner = runner
    
    def set_fitness(self, fitness, fitness_args=dict(), feasible_args=dict()):
        assert isinstance(fitness, Fitness)
        self.fitness = fitness
        self.fitness_args = fitness_args
        self.feasible_args = feasible_args
    

    def _evaluate(self, X, out, *args, **kwargs):
        assert hasattr(self, "runner")
        values = dict()
        for parameters in X:
            self.runner.set_parameters(parameters)
            self.runner.run(self.evaluation_period)

            results = self.fitness.fitness(**self.fitness_args)
            constraints = self.fitness.feasible(**self.feasible_args)

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

    def export_results(self, parameters, objectives, logger, folder):
        self.runner.set_parameters(parameters)
        self.runner.run(self.evaluation_period)

        processor = ResultsProcessor(logger)
        data = processor.plot({
            "reservoirs": ["current_volume", "overflow_volume"],
            "pumps": ["quantity"],
            "demands": ["quantity"],
        }, folder)

        processor.export_xslx(data, os.path.join(folder, "metrics.xlsx"))

        results = dict(
            X = self.runner.export_X(parameters),
            F = dict(
                energy = objectives[0],
                switches = objectives[1],
                volume_deltas = objectives[2],
            )
        )

        json.dump(results, open(os.path.join(folder, "results.json"), "w"))        

        