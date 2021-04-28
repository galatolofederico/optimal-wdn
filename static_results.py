import numpy as np
import pandas as pd
import argparse
import sys
import os

from src.problems import *
from src.runners import *
from src.experiments import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--experiment", type=str, default="ThresholdPrototypeExperiment")
    parser.add_argument("--save", type=str, default="")

    args = parser.parse_args()
    
    experiment = getattr(sys.modules[__name__], args.experiment)()

    X = np.array(experiment.runner.get_parameters())    

    out = dict()
    experiment.problem._evaluate(np.atleast_2d(X), out)
    F = out["F"][0]
    G = out["G"][0]

    if args.save != "":
        os.mkdir(args.save)
        experiment.problem.export_results(X, F, G, experiment.logger, args.save)