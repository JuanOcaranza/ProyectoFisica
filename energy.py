import pandas as pd
import numpy as np

class Energy:
    def __init__(self, df: pd.DataFrame, mass_weight: float, mass_forearm: float):
        self.df = df
        self._add_energy(mass_weight, mass_forearm)

    def _add_energy(self, mass_weight: float, mass_forearm: float):
        g = 9.81
        velocity_weight_squared = self.df['vy_wrist'] ** 2 + self.df['vx_wrist'] ** 2
        velocity_forearm_squared = self.df['vy_forearm'] ** 2 + self.df['vx_forearm'] ** 2

        self.df['potential_energy'] = mass_weight * g * self.df['ry_wrist'] + (
            mass_forearm * g * self.df['ry_forearm'])
        self.df['kinetic_energy'] = 0.5 * mass_weight * velocity_weight_squared + (
            0.5 * mass_forearm * velocity_forearm_squared)
        self.df['mechanical_energy'] = self.df['kinetic_energy'] + self.df['potential_energy']

    def get_work(self):
        self.df['work_i_from_energy'] = self.df['mechanical_energy'].diff()
        return np.sum(self.df['work_i_from_energy']), np.sum(np.abs(self.df['work_i_from_energy']))
