import numpy as np
import pandas as pd
import argparse
import pickle
import json
import sys
import os
from pymoo.factory import get_algorithm

from pymoo.optimize import minimize

from src.problems import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--problem", type=str, default="WaterDemandSequenceProblem")
    parser.add_argument("--algorithm", type=str, default="nsga2")
    parser.add_argument("--pop-size", type=int, default=100)
    parser.add_argument("--generations", type=int, default=1000)
    parser.add_argument("--save", type=str, default="")


    args = parser.parse_args()

    if args.save != "":
        assert not os.path.exists(args.save), "%s already exists" % (args.save)
        os.mkdir(args.save)

    problem = getattr(sys.modules[__name__], args.problem)()

    problem_algorithm_arguments = dict()
    if args.algorithm in problem.algorithm_arguments: problem_algorithm_arguments = problem.algorithm_arguments[args.algorithm]
    
    algorithm = get_algorithm(args.algorithm, pop_size=args.pop_size, **problem_algorithm_arguments)

    res = minimize(problem, algorithm, ("n_gen", args.generations), verbose=True)
    
    if args.save != "":
        pickle.dump(res, open(os.path.join(args.save, "results.pkl"), "wb"))
        json.dump(vars(args), open(os.path.join(args.save, "args.json"), "w"))