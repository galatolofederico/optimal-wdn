import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import os

class ResultsProcessor:
    def __init__(self, logger):
        self.logger = logger
    
    def plot(self, charts, folder):
        data = dict()
        for group_name, charts in charts.items():
            if group_name not in self.logger.history:
                continue
            metrics = self.logger.history[group_name]
            for chart in charts:
                name = "%s: %s" % (group_name, chart)
                
                series = list()
                for id, metric in metrics.items():
                    series.append(metric[chart])
                
                mpl.rcParams['figure.figsize'] = (8.0, 6.0)
                if len(series) > 5:
                    mpl.rcParams['figure.figsize'] = (10, 10)
                
                fig, axes = plt.subplots(len(series), 1)
                if len(series) == 1: axes = [axes]

                fig.suptitle(name)
                
                for s, ax in zip(series, axes):
                    x = [i["time"] for i in s]
                    y = [i["value"] for i in s]
                    ax.plot(x, y)

                fig.savefig(os.path.join(folder, "%s_%s.png" % (group_name, chart)))
                data["%s_%s" % (group_name, chart)] = series
        return data
    
    def export_xslx(self, data, file):
        df = None
        for name, series in data.items():
            for i, s in enumerate(series):
                times = [e["time"] for e in s]
                values = [e["value"] for e in s]
                series_df = pd.DataFrame(data={"time": times, "%s_%s" % (name, i): values})
                series_df = series_df.set_index("time")
                if df is None:
                    df = series_df
                else:
                    df = df.join(series_df)
        df.to_excel(file)