def position_columns(columns):
    return [column for column in columns if 'r' in column.split('_')[0]]

def velocity_columns(columns):
    return [column for column in columns if 'v' in column.split('_')[0]]

def acceleration_columns(columns):
    return [column for column in columns if 'a' in column.split('_')[0]]