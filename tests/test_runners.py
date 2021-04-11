import unittest
import numpy as np
import tempfile
import shutil

from tests.test_system import get_system

from src.simulator import *
from src import Logger, ResultsProcessor, Fitness
from src.runner import SequenceRunner, ThresholdRunner


class TestRunners(unittest.TestCase):
    def test_seq_runner(self):
        wds, elements = get_system(return_elements=True)


        runner = SequenceRunner(wds)

        p1_schedule = [0]*5 + [1]*7 + [0]*8 + [1]*4
        p2_schedule = p1_schedule

        assert len(p1_schedule) == 24
        assert len(p2_schedule) == 24

        schedule = np.stack([p1_schedule, p2_schedule]).T

        runner.set_parameters(schedule.flatten())
        runner.run(24)

        fitness = Fitness(wds.logger)
        print(fitness.fitness(reservoirs=[elements.tank], pumps=[elements.p1, elements.p2]))
        print(fitness.feasible(reservoirs=[elements.tank]))
        plotter = ResultsProcessor(wds.logger)

        save_dir = tempfile.mkdtemp()

        plotter.plot({
            "reservoirs": ["current_volume", "overflow_volume"],
            "pumps": ["quantity"],
            "demands": ["quantity"],
        }, save_dir)

        shutil.rmtree(save_dir)
    
    def test_th_runner(self):
        wds, elements = get_system(return_elements=True)

        runner = ThresholdRunner(wds, reservoirs=[elements.r1, elements.r2], on_thresholds=[10, 10], off_thresholds=[5, 5])
        runner.run(24*7)

        fitness = Fitness(wds.logger)
        print(fitness.fitness(reservoirs=[elements.tank], pumps=[elements.p1, elements.p2]))
        print(fitness.feasible(reservoirs=[elements.tank, elements.r1, elements.r2]))
        plotter = ResultsProcessor(wds.logger)

        save_dir = tempfile.mkdtemp()

        plotter.plot({
            "reservoirs": ["current_volume"],
            "pumps": ["quantity"],
            "demands": ["quantity"],
        }, save_dir)

        shutil.rmtree(save_dir)