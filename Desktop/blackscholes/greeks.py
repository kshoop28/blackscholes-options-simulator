import numpy as np
import pandas as pd
from scipy.stats import norm


def matrixcall(greek, sp, kp, rfr, vol, te):
    if greek == 'Delta':
        return deltacall(sp, kp, rfr, vol, te)
    elif greek == 'Gamma':
        return gammacall(sp, kp, rfr, vol, te)
    elif greek == 'Theta':
        return thetacall(sp, kp, rfr, vol, te)
    elif greek == 'Vega':
        return vegacall(sp, kp, rfr, vol, te)
        


def deltacall(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    return norm.cdf(d1)

def gammacall(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    return norm.pdf(d1) / (S__t * sigma * np.sqrt(t))

def thetacall(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    d2 = d1 - sigma * np.sqrt(t/365)
    return (-S__t * norm.pdf(d1) * sigma / 2 * np.sqrt(t)) - (r * K * np.exp(-r * t) * norm.cdf(d2))

def vegacall(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    return S__t * np.sqrt(t) * norm.pdf(d1)
    
def matrixput(greek, sp, kp, rfr, vol,  te):
    if greek == 'Delta':
        return deltaput(sp,kp,rfr,vol,te)
    elif greek == 'Gamma':
        return gammaput(sp,kp,rfr,vol,te)
    elif greek == 'Theta':
        return thetaput(sp,kp,rfr,vol,te)
    elif greek == 'Vega':
        return vegaput(sp,kp,rfr,vol,te)


def deltaput(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    return norm.cdf(d1) - 1

def gammaput(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    return norm.pdf(d1) / (S__t * sigma * np.sqrt(t))

def thetaput(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    d2 = d1 - sigma * np.sqrt(t/365)
    return (-S__t * norm.pdf(d1) * sigma / 2 * np.sqrt(t)) + (r * K * np.exp(-r * t) * norm.cdf(-d2))
    

def vegaput(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    return S__t * np.sqrt(t) * norm.pdf(d1)


    
    
    
