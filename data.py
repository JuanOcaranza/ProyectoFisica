import pandas as pd
from datetime import datetime
import numpy as np
from filter import Filter

class Data:
    def __init__(self, df, objects):
        self.df = df
        self.objects = objects
        self.filter = Filter()
        self._add_velocity()
        self._add_acceleration()
        self.add_polar_wrist()
        self.add_angular_velocity()

    def _add_velocity(self):
        self.df = self.filter.apply_filter(self.df.columns, self.df)
        for object in self.objects:
            self.df[f"vx_{object}"] = self.df[f"rx_{object}"].diff()
            self.df[f"vy_{object}"] = self.df[f"ry_{object}"].diff()
    
    def _add_acceleration(self):
        self.df = self.filter.apply_filter([column for column in self.df.columns if 'v' in column], self.df)
        for object in self.objects:
            self.df[f"ax_{object}"] = self.df[f"vx_{object}"].diff()
            self.df[f"ay_{object}"] = self.df[f"vy_{object}"].diff()
        self.df = self.filter.apply_filter([column for column in self.df.columns if 'a' in column], self.df)
    
    def add_polar_wrist(self):
        x_vector_elbow_to_wrist = self.df['rx_wrist'] - self.df['rx_elbow']
        y_vector_elbow_to_wrist = self.df['ry_wrist'] - self.df['ry_elbow']
        magnitude_vector_elbow_to_wrist = np.sqrt(x_vector_elbow_to_wrist ** 2 + y_vector_elbow_to_wrist ** 2)
        x_vector_elbow_to_shoulder = self.df['rx_shoulder'] - self.df['rx_elbow']
        y_vector_elbow_to_shoulder = self.df['ry_shoulder'] - self.df['ry_elbow']
        magnitude_vector_elbow_to_shoulder = np.sqrt(x_vector_elbow_to_shoulder ** 2 + y_vector_elbow_to_shoulder ** 2)
        elbow_to_wrist_scalar_product_elbow_to_shoulder = x_vector_elbow_to_wrist * x_vector_elbow_to_shoulder + y_vector_elbow_to_wrist * y_vector_elbow_to_shoulder
        cosine_angle = elbow_to_wrist_scalar_product_elbow_to_shoulder / (magnitude_vector_elbow_to_wrist * magnitude_vector_elbow_to_shoulder)
        self.df['r_wrist'] = magnitude_vector_elbow_to_wrist
        self.df['theta_wrist'] = np.arccos(cosine_angle)
    
    def add_angular_velocity(self):
        self.df['angular_velocity'] = self.df['theta_wrist'].diff()

    def get_data(self, save = False):
        if save:
            self.df.to_csv(f"csv/data{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index = False)
        return self.df
