import pandas as pd
import numpy as np

class Forces:
    def __init__(self, df, mass):
        self.df = df
        self.mass = mass
        self._add_forces()
    
    def _add_forces(self):
        self.df['fx_total'] = self.mass * self.df['ax_wrist']
        self.df['fy_total'] = self.mass * self.df['ay_wrist']
        self.df['fx_g'] = 0
        self.df['fy_g'] = self.mass * -9.81
        self.df['fx_not_g'] = self.df['fx_total']
        self.df['fy_not_g'] = self.df['fy_total'] - self.df['fy_g']

    def get_data_with_forces(self):
        return self.df