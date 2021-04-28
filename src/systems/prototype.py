from src.simulator import *
from src import Logger, Fitness, ResultsProcessor

def get_prototype():
    d1_demand = [1.32, 1.32, 0.936, 0.936, 0.936, 2.352, 2.352, 2.352, 2.352, 0.936, 0.936, 1.32, 1.32, 1.32, 1.32, 1.32, 0.402, 0.402, 0.402, 0.402, 0.402, 0.402, 0.402, 0.402]
    d2_demand = [0.924, 0.924, 2.01, 2.01, 2.01, 2.454, 2.454, 2.454, 2.454, 1.44, 1.44, 2.01, 2.01, 2.01, 2.01, 2.01, 0.414, 0.414, 0.414, 0.414, 0.414, 0.414, 0.414, 0.414]

    wds = System(dt=1)

    tank = Reservoir(system=wds, max_volume=30, min_volume=10, initial_volume=30)
    r1 = Reservoir(system=wds, max_volume=14, min_volume=4, initial_volume=4)
    r2 = Reservoir(system=wds, max_volume=14, min_volume=4, initial_volume=4)

    p1 = Pump(source=r1, destination=tank, flow=3, power=8)
    p2 = Pump(source=r2, destination=tank, flow=3, power=8)

    d1 = LoopbackStaticDemand(demand=d1_demand, source=tank, destination=r1)
    d2 = LoopbackStaticDemand(demand=d2_demand, source=tank, destination=r2)

    logger = Logger(groups={
        "reservoirs": [tank, r1, r2],
        "pumps": [p1, p2],
        "demands": [d1, d2],
    })

    wds.add_logger(logger)
    fitness = Fitness(logger)

    return dict(
        system=wds,
        logger=logger,
        fitness=fitness
    )