import pandas as pd
import numpy as np
from . import filter as ft
from . import column_filter as cf

class Data:
    def __init__(self, df: pd.DataFrame, objects: list):
        self.df = df
        self.objects = objects
        self._add_velocity()
        self._add_acceleration()
        self._add_polar_wrist()
        self._add_angular_velocity()
        self._add_angular_acceleration()
        self._add_time()
        self._add_other_positions()

    def _add_velocity(self):
        self.df = ft.apply_filter(self.df, self.df.columns)
        for object in self.objects:
            self.df[f"vx_{object}"] = self.df[f"rx_{object}"].diff()
            self.df[f"vy_{object}"] = self.df[f"ry_{object}"].diff()
    
    def _add_acceleration(self):
        self.df = ft.apply_filter(self.df, cf.velocity_columns(self.df.columns))
        for object in self.objects:
            self.df[f"ax_{object}"] = self.df[f"vx_{object}"].diff()
            self.df[f"ay_{object}"] = self.df[f"vy_{object}"].diff()
        self.df = ft.apply_filter(self.df, cf.acceleration_columns(self.df.columns))
    
    def _add_polar_wrist(self):
        x_vector_elbow_to_wrist = self.df['rx_wrist'] - self.df['rx_elbow']
        y_vector_elbow_to_wrist = self.df['ry_wrist'] - self.df['ry_elbow']
        magnitude_vector_elbow_to_wrist = np.sqrt(x_vector_elbow_to_wrist ** 2 + y_vector_elbow_to_wrist ** 2)
        x_vector_elbow_to_shoulder = self.df['rx_shoulder'] - self.df['rx_elbow']
        y_vector_elbow_to_shoulder = self.df['ry_shoulder'] - self.df['ry_elbow']
        magnitude_vector_elbow_to_shoulder = np.sqrt(x_vector_elbow_to_shoulder ** 2 + y_vector_elbow_to_shoulder ** 2)
        elbow_to_wrist_scalar_product_elbow_to_shoulder = x_vector_elbow_to_wrist * x_vector_elbow_to_shoulder + y_vector_elbow_to_wrist * y_vector_elbow_to_shoulder
        cosine_angle = elbow_to_wrist_scalar_product_elbow_to_shoulder / (magnitude_vector_elbow_to_wrist * magnitude_vector_elbow_to_shoulder)
        self.df['r_wrist'] = magnitude_vector_elbow_to_wrist
        self.df = ft.apply_filter(self.df, ['r_wrist'])
        self.df['theta_wrist'] = np.arccos(cosine_angle)
        self.df = ft.apply_filter(self.df, ['theta_wrist'])


        self.df['distance_elbow_shoulder'] = magnitude_vector_elbow_to_shoulder
        self.df['x_vector_elbow_to_shoulder'] = x_vector_elbow_to_shoulder
        self.df['y_vector_elbow_to_shoulder'] = y_vector_elbow_to_shoulder
        
        distance_shoulder_vertical = self.df['rx_shoulder'] - self.df['rx_elbow']
        sin_angle_upperarm_vertical = distance_shoulder_vertical / magnitude_vector_elbow_to_shoulder
        self.df['angle_upperarm_vertical'] = np.arcsin(sin_angle_upperarm_vertical)

        distance_wrist_horizontal = self.df['ry_wrist'] - self.df['ry_elbow']
        sin_angle_forarm_horizontal = distance_wrist_horizontal / magnitude_vector_elbow_to_wrist
        self.df['angle_forearm_horizontal'] = np.arcsin(sin_angle_forarm_horizontal)

        self.df['angle_forearm_vertical'] = self.df['theta_wrist'] + self.df['angle_upperarm_vertical']
        self.df['angle_upperarm_horizontal'] = self.df['theta_wrist'] + self.df['angle_forearm_horizontal']
    
    def _add_angular_velocity(self):
        self.df['angular_velocity'] = self.df['theta_wrist'].diff()
        self.df = ft.apply_filter(self.df, ['angular_velocity'])

    def _add_angular_acceleration(self):
        self.df['angular_acceleration'] = self.df['angular_velocity'].diff()
        self.df = ft.apply_filter(self.df, ['angular_acceleration'])
    
    def _add_time(self):
        self.df['time'] = self.df.index

    def _add_other_positions(self):
        self.df['rx_forearm'] = self.df['rx_elbow'] + ((self.df['rx_wrist'] - self.df['rx_elbow']) / 2)
        self.df['ry_forearm'] = self.df['ry_elbow'] + ((self.df['ry_wrist'] - self.df['ry_elbow']) / 2)

    def get_data(self):
        return self.df
