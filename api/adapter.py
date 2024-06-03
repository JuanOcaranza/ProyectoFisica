import pandas as pd

class Adapter:
    def __init__(self, positions: list, objects: list, window_height: float):
        self.window_height = window_height
        self.df = pd.DataFrame(positions, columns = objects)
        self._split_columns(objects)
        self._move_catesian_origin_to_bottom_left([f"ry_{column}" for column in objects])

    def _split_columns(self, columns: list):
        for column in columns:
            self.df[[f"rx_{column}", f"ry_{column}"]] = self.df[column].apply(pd.Series)
            self.df.drop(columns = [column], inplace = True)

    def _move_catesian_origin_to_bottom_left(self, columns: list):
        for column in columns:
            self.df[column] = self.window_height - self.df[column]

    def get_adapted_data(self):
        return self.df