import os
import sys
import json
import argparse
import pickle
from pymoo.factory import get_decision_making

from src.problems import *

parser = argparse.ArgumentParser()

parser.add_argument("--folder", type=str, required=True)

args = parser.parse_args()

decision_making_strategies = dict(
    pw_all=("pseudo-weights", [.33, .33, .33]),
    pw_energy=("pseudo-weights", [.9, .05, .05]),
    pw_switches=("pseudo-weights", [.05, .9, .05]),
    pw_volume=("pseudo-weights", [.05, .05, .9])
)

res = pickle.load(open(os.path.join(args.folder, "results.pkl"), "rb"))
problem_args = json.load(open(os.path.join(args.folder, "args.json"), "r"))

vars(args).update(problem_args)

problem = getattr(sys.modules[__name__], args.problem)()

for name, strategy in decision_making_strategies.items():
    result = get_decision_making(*strategy).do(res.F)
    os.mkdir(os.path.join(args.folder, name))
    problem.export_results(res.X[result], res.F[result], os.path.join(args.folder, name))