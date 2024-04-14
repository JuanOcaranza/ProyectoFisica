import pandas as pd

class Adapter:
    def __init__(self, positions, columns, window_heigh):
        self.window_heigh = window_heigh
        self.df = pd.DataFrame(positions, columns = columns)
        self._split_columns(columns)
        self._move_catesian_origin_to_bottom_left([f"ry_{column}" for column in columns])

    def _split_columns(self, columns):
        for column in columns:
            self.df[[f"rx_{column}", f"ry_{column}"]] = self.df[column].apply(pd.Series)
            self.df.drop(columns = [column], inplace=True)

    def _move_catesian_origin_to_bottom_left(self, columns):
        for column in columns:
            self.df[column] = self.window_heigh - self.df[column]

    def get_adapted_data(self):
        return self.df