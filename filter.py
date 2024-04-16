from scipy.signal import savgol_filter

class Filter:
    
    def apply_filter(self, columns,data):
        for item in columns:
            data[item] = savgol_filter(data[item], window_length=9, polyorder=1)
        return data