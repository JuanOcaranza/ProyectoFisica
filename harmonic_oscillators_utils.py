import numpy as np

def omega_0(k, m):
    return np.sqrt(k/m)

def period(omega):
    return 2 * np.pi / omega