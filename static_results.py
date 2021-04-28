import numpy as np
import pandas as pd
import argparse
import sys
import os

from src.problems import *
from src.runners import *
from src.systems import *

from configs import configs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, default="prototype_th")
    parser.add_argument("--save", type=str, default="")

    args = parser.parse_args()
    
    assert args.config in configs
    config = configs[args.config]

    problem = config["problem"]["type"](**config["problem"]["args"])
    system = config["system"]["type"](**config["system"]["args"])

    runner = config["runner"]["type"](system["system"], **config["runner"]["args"])
    
    

    assert False
    out = dict()
    problem._evaluate(np.atleast_2d(X), out)
    F = out["F"][0]

    if args.save != "":
        os.mkdir(args.save)
        problem.export_results(X, F, args.save)