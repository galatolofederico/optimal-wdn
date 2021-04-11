import numpy as np
import pandas as pd
import argparse
import pickle
import os
import sys
import json


from src.problems import *

parser = argparse.ArgumentParser()

parser.add_argument("--folder", type=str, required=True)
parser.add_argument("--export-pseudo-weights", action="store_true")

args = parser.parse_args()

res = pickle.load(open(os.path.join(args.folder, "results.pkl"), "rb"))
problem_args = json.load(open(os.path.join(args.folder, "args.json"), "r"))

vars(args).update(problem_args)

problem = getattr(sys.modules[__name__], args.problem)()

names = problem.get_names()
x_df = pd.DataFrame(data=res.X, columns=["X_%d" % (i, ) for i in range(0, res.X.shape[1])])
f_df = pd.DataFrame(data=res.F, columns=["f_%s" % (n, ) for n in names["objectives"]])
g_df = pd.DataFrame(data=res.G, columns=["g_%s" % (n, ) for n in names["constraints"]])

dataframes = [x_df, f_df, g_df]

if args.export_pseudo_weights:
    from pymoo.factory import get_decision_making
    _, pseudo_weights = get_decision_making("pseudo-weights", [0, 0, 0]).do(res.F, return_pseudo_weights=True)
    pw_df = pd.DataFrame(data=pseudo_weights, columns=["pw_%s" % (n, ) for n in names["objectives"]])

    dataframes.append(pw_df)

results_df = pd.concat(dataframes, axis=1)
results_df.to_excel(os.path.join(args.save, "results.xlsx"))