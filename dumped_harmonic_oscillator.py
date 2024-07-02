import numpy as np

def k_1(kv, m):
    return kv / m

def alpha(k1):
    return k1 / 2

def behavior(omega_0, alpha):
    if omega_0 > alpha:
        return "underdamped"
    elif omega_0 < alpha:
        return "overdamped"
    else:
        return "critically damped"

def Omega(omega_0, alpha):
    return np.sqrt(omega_0 ** 2 - alpha ** 2)
    
def underdamped_position(alpha, t, x0, v0, Omega):
    return np.exp(- alpha * t) * (x0 * np.cos(Omega * t) + v0 / Omega * np.sin(Omega * t))

def Omega_prima(omega_0, alpha):
    return np.sqrt(alpha ** 2 - omega_0 ** 2)