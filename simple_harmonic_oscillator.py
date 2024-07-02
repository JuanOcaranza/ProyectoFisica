import numpy as np

def position(a, omega, t, phi = 0):
    return a * np.sin(omega * t + phi)

def time_from_position(a, omega, x, phi = 0):
    return (np.arcsin(x / a) - phi) / omega

def velocity(a, omega, t, phi = 0):
    return a * omega * np.cos(omega * t + phi)

def acceleration(a, omega, t, phi = 0):
    return -a * omega**2 * np.sin(omega * t + phi)

def acceleration_from_poisition(k, m, x):
    return - k * x / m

def phi(omega, x_0, v_0):
    return np.arctan2(x_0 * omega, v_0)

def aplitude(omega, x_0, v_0):
    return np.sqrt(x_0 ** 2 + (v_0 / omega) ** 2)