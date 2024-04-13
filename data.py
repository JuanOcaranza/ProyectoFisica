import pandas as pd

class Data:
    def __init__(self, objects, cartesian_positions):
        self.df = pd.DataFrame(cartesian_positions, columns = objects)
        self.objects = objects
        for object in objects:
            self._split_positions(object)
        self._add_velocity()
        self._add_acceleration()

    def _split_positions(self, object):
        self.df[[f"rx_{object}", f"ry_{object}"]] = self.df[object].apply(pd.Series)
        self.df.drop(columns = [object], inplace=True)

    def _add_velocity(self):
        for object in self.objects:
            self.df[f"vx_{object}"] = self.df[f"rx_{object}"].diff()
            self.df[f"vy_{object}"] = self.df[f"ry_{object}"].diff()
    
    def _add_acceleration(self):
        for object in self.objects:
            self.df[f"ax_{object}"] = self.df[f"vx_{object}"].diff()
            self.df[f"ay_{object}"] = self.df[f"vy_{object}"].diff()

    def get_data(self):
        return self.df
