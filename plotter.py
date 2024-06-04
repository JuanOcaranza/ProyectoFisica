import plotly.subplots as sp
import plotly.graph_objects as go
import pandas as pd

class Plotter:
    def __init__(self, df: pd.DataFrame):
        self.fig = sp.make_subplots(specs = [[{'secondary_y': True}]])

        for column in df.columns:
            if column == 'time':
                continue
            self.fig.add_trace(go.Line(
                x = df['time'], y = df[column], name = column), secondary_y = False)

    def show_plot(self):
        self.fig.show()
