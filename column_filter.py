import re

def position_columns(columns):
    return [column for column in columns if re.match("r.?_", column)]

def velocity_columns(columns):
    return [column for column in columns if re.match("v.?_", column)]

def acceleration_columns(columns):
    return [column for column in columns if re.match("a.?_", column)]
