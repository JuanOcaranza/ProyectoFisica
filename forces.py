import numpy as np
import pandas as pd

class Forces:
    def __init__(self, df: pd.DataFrame, mass_forearm: float, mass_weight: float, radius_bicep: float):
        self.df = df
        self.radius_bicep = radius_bicep
        self._add_force_bicep(mass_forearm, mass_weight)

    def _add_force_bicep(self, mass_forearm: float, mass_weight: float):
        g = -9.81

        radius_weight = self.df['r_wrist']
        radius_forearm = radius_weight / 2

        inertia_weight = mass_weight * radius_weight ** 2
        inertia_forearm = mass_forearm * radius_forearm ** 2

        sum_moment = (inertia_weight + inertia_forearm) * self.df['angular_acceleration']

        angle_forearm_g = np.pi - self.df['theta_wrist']
        moment_weight = radius_weight * mass_weight * g * np.sin(angle_forearm_g)
        moment_forearm = radius_forearm * mass_forearm * g * np.sin(angle_forearm_g)

        self.df['force_bicep'] = (sum_moment - moment_weight - moment_forearm) / (self.radius_bicep * np.sin(self.df['theta_wrist']))
        
        self.df['sum_moment'] = sum_moment
        self.df['moment_weight'] = moment_weight
        self.df['moment_forearm'] = moment_forearm

        self.df['px_weight'] = 0
        self.df['py_weight'] = mass_weight * g

        self.df['px_forearm'] = 0
        self.df['py_forearm'] = mass_forearm * g

        self.df['rx_bicep'] = self.df['rx_elbow'] + self.radius_bicep * np.cos(self.df['angle_forearm_horizontal'])
        self.df['ry_bicep'] = self.df['ry_elbow'] + self.radius_bicep * np.cos(self.df['angle_forearm_vertical'])
        self.df['fx_bicep'] = self.df['force_bicep'] * np.cos(self.df['angle_upperarm_horizontal'])
        self.df['fy_bicep'] = self.df['force_bicep'] * np.cos(self.df['angle_upperarm_vertical'])

    def get_data_with_forces(self):
        return self.df
    
    def get_work(self):
        angle_bicep_movement = np.abs(np.pi / 2 - self.df['theta_wrist'])
        projected_force = self.df['force_bicep'] * np.cos(angle_bicep_movement)
        
        distance = np.sqrt(self.df['distance_elbow_shoulder'] ** 2 + self.radius_bicep ** 2 -
                           2 * self.df['distance_elbow_shoulder'] * self.radius_bicep *
                           np.cos(self.df['theta_wrist']))
        delta_distance = distance.diff()
 
        work_i = projected_force * delta_distance
        work_i_abs = np.abs(work_i)

        self.df['work_i'] = work_i

        self.df['distance_bicep'] = distance
        
        return np.sum(work_i), np.sum(work_i_abs)
