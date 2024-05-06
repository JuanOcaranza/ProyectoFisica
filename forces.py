import numpy as np

class Forces:
    def __init__(self, df, mass_forearm, mass_weight, radius_bicep):
        self.df = df
        self.radius_bicep = radius_bicep
        self._add_force_bicep(mass_forearm, mass_weight)

    def _add_force_bicep(self, mass_forearm, mass_weight):
        g = -9.81

        radius_weight = self.df['r_wrist']
        radius_forearm = radius_weight / 2

        inertia_weight = mass_weight * radius_weight ** 2
        inertia_forearm = mass_forearm * radius_forearm ** 2

        sum_moment = (inertia_weight + inertia_forearm) * self.df['angular_acceleration']

        angle_forearm_g = np.pi - self.df['theta_wrist']
        moment_weight = radius_weight * mass_weight * g * np.cos(angle_forearm_g)
        moment_forearm = radius_forearm * mass_forearm * g * np.cos(angle_forearm_g)

        self.df['force_bicep'] = (sum_moment - moment_weight - moment_forearm) / (self.radius_bicep * np.cos(self.df['theta_wrist']))
        
        self.df['sum_moment'] = sum_moment
        self.df['moment_weight'] = moment_weight
        self.df['moment_forearm'] = moment_forearm

    def get_data_with_forces(self):
        return self.df
    
    def get_work(self):
        angle_bicep_movement = np.abs(np.pi / 2 - self.df['theta_wrist'])
        projected_force = self.df['force_bicep'] * np.cos(angle_bicep_movement)
        differential_distance = self.radius_bicep * self.df['angular_velocity']
        work_i = projected_force * differential_distance
        
        return np.sum(work_i)
