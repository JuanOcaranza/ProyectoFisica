import pandas as pd
import numpy as np
import filter as ft
import column_filter as cf

class Data:
    def __init__(self, df, objects):
        self.df = df
        self.objects = objects
        self._add_velocity()
        self._add_acceleration()
        self._add_polar_wrist()
        self._add_angular_velocity()
        self._add_angular_acceleration()
        self._add_time()

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
    
    def _add_angular_velocity(self):
        self.df['angular_velocity'] = self.df['theta_wrist'].diff()
        self.df = ft.apply_filter(self.df, ['angular_velocity'])

    def _add_angular_acceleration(self):
        self.df['angular_acceleration'] = self.df['angular_velocity'].diff()
        self.df = ft.apply_filter(self.df, ['angular_acceleration'])
    
    def _add_time(self):
        self.df['time'] = self.df.index

    def get_data(self):
        return self.df
