from scipy.signal import savgol_filter

def apply_filter(data, columns):
    for item in columns:
        data[item] = savgol_filter(data[item], window_length = 9, polyorder = 1)
    return data
