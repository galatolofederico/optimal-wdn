import os
import argparse
import pickle
from pymoo.visualization.scatter import Scatter


parser = argparse.ArgumentParser()

parser.add_argument("--folder", type=str, required=True)

args = parser.parse_args()

res = pickle.load(open(os.path.join(args.folder, "results.pkl"), "rb"))

print(res.X)

plot = Scatter(labels=["energy", "switches", "volume_deltas"])
plot.add(res.F, color="red")
plot.show()