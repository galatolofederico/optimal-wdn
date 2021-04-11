import unittest
import random
import tempfile
import shutil

from types import SimpleNamespace

from src.simulator import *
from src import Logger, ResultsProcessor

def get_system(return_elements=False):
    d1_demand = [0.022, 0.022, 0.0156, 0.0156, 0.0156, 0.0392, 0.0392, 0.0392, 0.0392, 0.0156, 0.0156, 0.022, 0.022, 0.022, 0.022, 0.022, 0.0067, 0.0067, 0.0067, 0.0067, 0.0067, 0.0067, 0.0067, 0.0067]
    d2_demand = [0.0154, 0.0154, 0.0335, 0.0335, 0.0335, 0.0409, 0.0409, 0.0409, 0.0409, 0.024, 0.024, 0.0335, 0.0335, 0.0335, 0.0335, 0.0335, 0.0069, 0.0069, 0.0069, 0.0069, 0.0069, 0.0069, 0.0069, 0.0069]

    wds = System(dt=1)

    tank = Reservoir(system=wds, max_volume=100, initial_volume=50)
    r1 = Reservoir(system=wds, max_volume=20, initial_volume=5)
    r2 = Reservoir(system=wds, max_volume=20, initial_volume=15)

    p1 = Pump(source=r1, destination=tank, flow=2)
    p2 = Pump(source=r2, destination=tank, flow=2)

    d1 = LoopbackStaticDemand(demand=d1_demand, source=tank, destination=r1)
    d2 = LoopbackStaticDemand(demand=d2_demand, source=tank, destination=r2)

    logger = Logger(groups={
        "reservoirs": [tank, r1, r2],
        "pumps": [p1, p2],
        "demands": [d1, d2],
    })

    wds.add_logger(logger)
    wds.reset()
    if return_elements:
        return wds, SimpleNamespace(tank=tank, r1=r1, r2=r2, p1=p1, p2=p2, d1=d1, d2=d2)
    return wds



class TestSystem(unittest.TestCase):
    def test_system(self):
        wds, elements = get_system(return_elements=True)

        off_volume = 5
        on_volume = 10
        state_p1 = 0
        state_p2 = 0
        for i in range(0, 24*7):
            if elements.r1.current_volume < off_volume:
                state_p1 = 0
            if elements.r1.current_volume > on_volume:
                state_p1 = 1
            if elements.r2.current_volume < off_volume:
                state_p2 = 0
            if elements.r2.current_volume > on_volume:
                state_p2 = 1
            
            actions = [state_p1, state_p2]
            wds.step(actions)

        plotter = ResultsProcessor(wds.logger)

        save_dir = tempfile.mkdtemp()
        plotter.plot({
            "reservoirs": ["current_volume"],
            "pumps": ["quantity"],
            "demands": ["quantity"],
        }, save_dir)
        shutil.rmtree(save_dir)