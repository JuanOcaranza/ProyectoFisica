import pandas as pd
import numpy as np

class Energy:
    def __init__(self, df: pd.DataFrame, mass, height_shoulder):
        self.df = df
        self._add_energy(mass, height_shoulder)

    def _add_energy(self, mass, height_shoulder):
        g = 9.81
        height_weight = height_shoulder - self.df['ry_shoulder'] + self.df['ry_wrist']
        velocity = np.sqrt(self.df['vy_wrist'] ** 2 + self.df['vx_wrist'] ** 2)

        self.df['potential_energy'] = mass * g * height_weight
        self.df['kinetic_energy'] = 0.5 * mass * velocity ** 2
        self.df['mechanical_energy'] = self.df['kinetic_energy'] + self.df['potential_energy']
    
    def get_work(self):
        self.df['work_i_from_energy'] = self.df['mechanical_energy'].diff()
        return np.sum(self.df['work_i_from_energy']), np.sum(np.abs(self.df['work_i_from_energy']))