import pandas as pd
from datetime import datetime

class Data:
    def __init__(self, df, objects):
        self.df = df
        self.objects = objects
        self._add_velocity()
        self._add_acceleration()

    def _add_velocity(self):
        for object in self.objects:
            self.df[f"vx_{object}"] = self.df[f"rx_{object}"].diff()
            self.df[f"vy_{object}"] = self.df[f"ry_{object}"].diff()
    
    def _add_acceleration(self):
        for object in self.objects:
            self.df[f"ax_{object}"] = self.df[f"vx_{object}"].diff()
            self.df[f"ay_{object}"] = self.df[f"vy_{object}"].diff()

    def get_data(self, save = False):
        if save:
            self.df.to_csv(f"csv/data{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index = False)
        return self.df