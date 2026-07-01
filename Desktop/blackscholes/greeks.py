import numpy as np
import pandas as pd
from scipy.stats import norm


class op:
    def __init__(self, S__t, K, r, sigma, t):
        self.S__t = S__t
        self.K = K
        self.r = r
        self.sigma = sigma
        self.t = t / 365
    
    @property
    def d1(self):
        return (np.log(self.S__t / self.K) + (self.r + (self.sigma**2 / 2)) * (self.t)) / (self.sigma * np.sqrt(self.t))
    
    @property
    def d2(self):
        return self.d1 - self.sigma * np.sqrt(self.t)
        
    #Delta Calls and Puts
    
    def deltacall(self):
        return norm.cdf(self.d1)
    
    def deltaput(self):
        return norm.cdf(self.d1) -1
    
    #Gamma Calls and Puts
    
    def gammacall(self):
        return norm.pdf(self.d1) / (self.S__t * self.sigma * np.sqrt(self.t)) 

    def gammaput(self):
        return norm.pdf(self.d1) / (self.S__t * self.sigma * np.sqrt(self.t))
        
    #Theta Calls and Puts

    def thetacall(self):
        return (-self.S__t * norm.pdf(self.d1) * self.sigma / 2 * np.sqrt(self.t)) - (self.r * self.K * np.exp(-self.r * self.t) * norm.cdf(self.d2))
    
    def thetaput(self):
        return (-self.S__t * norm.pdf(self.d1) * self.sigma / 2 * np.sqrt(self.t)) + (self.r * self.K * np.exp(-self.r * self.t) * norm.cdf(-self.d2))

    # Vega Calls and Puts
    
    def vegacall(self):
        return self.S__t * np.sqrt(self.t) * norm.pdf(self.d1)
    
    def vegaput(self):
        return self.S__t * np.sqrt(self.t) * norm.pdf(self.d1)
    




    
    
    
def matrixcall(greek, sp, kp, rfr, vol, te):
    option = op(sp, kp, rfr, vol, te)
    if greek == 'Delta':
        return option.deltacall()
    elif greek == 'Gamma':
        return option.gammacall()
    elif greek == 'Theta':
        return option.thetacall()
    elif greek == "Vega":
        return option.vegacall()

def matrixput(greek, sp, kp, rfr, vol, te):
    option = op(sp, kp, rfr, vol, te)
    if greek == 'Delta':
        return option.deltaput()
    elif greek == 'Gamma':
        return option.gammaput()
    elif greek == 'Theta':
        return option.thetaput()
    elif greek == "Vega":
        return option.vegaput()
    
    
