from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

class Fitter:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self._add_fitted_curves()

    def _add_fitted_curves(self):
        a0, b0, c0, d0 = self._pre_fit()
        self.df['curve_fit_0'] = _sin(self.df['time'], a0, b0, c0, d0)

        sin_b = _sin_generator_b(a0, c0, d0)
        poptB, pcov = curve_fit(sin_b, self.df['time'], self.df['theta_wrist'], b0, method="dogbox")
        b = poptB[0]
        self.df['curve_fit_post_b'] = _sin(self.df['time'], a0, b, c0, d0)
        
        sin_d = _sin_generator_d(a0, b, c0)
        poptD, pcov = curve_fit(sin_d, self.df['time'], self.df['theta_wrist'], d0, method="dogbox")
        d = poptD[0]
        self.df['curve_fit_post_d'] = _sin(self.df['time'], a0, b, c0, d)

        sin_c = _sin_generator_c(a0, b, d)
        poptC, pcov = curve_fit(sin_c, self.df['time'], self.df['theta_wrist'], c0, method="dogbox")
        c = poptC[0]
        self.df['curve_fit_post_c'] = _sin(self.df['time'], a0, b, c, d)

        sin_a = _sin_generator_a(b, c, d)
        poptA, pcov = curve_fit(sin_a, self.df['time'], self.df['theta_wrist'], a0, method="dogbox")
        a = poptA[0]

        self.df['curve_fit_theta'] = _sin(self.df['time'], a, b, c, d)
    
    def _pre_fit(self):
        a = self._pre_fit_a()
        b = self._pre_fit_b()
        d = self._pre_fit_d(a)
        c = self._pre_fit_c(a, d)
        return a, b, c, d
    
    def _pre_fit_a(self):
        return self.df['theta_wrist'].mean() / 2

    def _pre_fit_b(self):
        return self.df['angular_velocity'].abs().mean()
        
    def _pre_fit_d(self, a):
        return a + self.df['theta_wrist'].min()
    
    def _pre_fit_c(self, a, d):
        return np.arcsin(min(((self.df['theta_wrist'].iloc[0] - d) / a), 1))

    def get_df(self):
        return self.df
    
def _sin_generator_a(b, c, d):
    return lambda x, a: a * np.sin(b * x + c) + d

def _sin_generator_b(a, c, d):
    return lambda x, b: a * np.sin(b * x + c) + d

def _sin_generator_c(a, b, d):
    return lambda x, c: a * np.sin(b * x + c) + d

def _sin_generator_d(a, b, c):
    return lambda x, d: a * np.sin(b * x + c) + d

def _sin(x, a, b, c, d):
        return a * np.sin(b * x + c) + d
