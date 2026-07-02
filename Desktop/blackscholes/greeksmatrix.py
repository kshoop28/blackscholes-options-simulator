import numpy as np
import streamlit as st
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt



def matcall(gr, stockprice, K, r, volatility, t):
    try:
        pcurrent = int(stockprice)
        vcurrent = int(round(volatility * 100))
        matrix = []

        pstartvalue = max(1, pcurrent - 5)

        vstartvalue = max(1, vcurrent - 5)
        
        
        pendvalue = pcurrent + 5

        vendvalue = vcurrent + 5


        p10 = list(range(pstartvalue, pendvalue + 1))
        v10 = list(range(vstartvalue, vendvalue +1))
        
        t = t/365


        for p in p10:
            row = []    
            for v in v10:
                sigma = v / 100
                d1 =  (np.log(p / K) + (r + (sigma**2 / 2)) * (t)) / (sigma * np.sqrt(t))
                d2 =  (d1 - sigma * np.sqrt(t))
                
                if gr == 'Delta':
                    value = norm.cdf(d1)
                elif gr == 'Gamma':
                    value = norm.pdf(d1) / (p * sigma * np.sqrt(t)) 
                elif gr == 'Theta':
                    value = (-p * norm.pdf(d1) * sigma / 2 * np.sqrt(t)) - (r * K * np.exp(r * t) * norm.cdf(d2))
                elif gr == 'Vega':
                    value = p * np.sqrt(t) * norm.pdf(d1)
                row.append(value)
            matrix.append(row)
            
        df = pd.DataFrame(matrix, index = p10, columns = v10)

        df.index.name = 'Underlying Prices'
        df.columns.name = 'Implied Volatility (%)'
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(df, annot=True,fmt=".3f",ax =ax)
        
        if gr == 'Delta':
            ax.set_title('Delta Call Sensitivity Matrix')
        elif gr == 'Gamma':
            ax.set_title('Gamma Call Sensitivity Matrix')
        elif gr == 'Theta':
            ax.set_title('Theta Call Sensitivity Matrix')
        elif gr == 'Vega':
            ax.set_title('Vega Call Sensitivity Matrix')
        return fig
        
    except ValueError:
        pass
        
    
def matput(ar, stockprice, K, r, volatility, t):
    try:
        pcurrent = int(stockprice)
        vcurrent = int(round(volatility * 100))
        matrix = []

        pstartvalue = max(1, pcurrent - 5)

        vstartvalue = max(1, vcurrent - 5)
        
        
        pendvalue = pcurrent + 5

        vendvalue = vcurrent + 5


        p10 = list(range(pstartvalue, pendvalue + 1))
        v10 = list(range(vstartvalue, vendvalue +1))
        
        t = t / 365



        for p in p10:
            row = []    
            for v in v10:
                sigma = v / 100
                d1 =  (np.log(p / K) + (r + (sigma**2 / 2)) * (t)) / (sigma * np.sqrt(t))
                d2 =  (d1 - sigma * np.sqrt(t))
                     
                if ar == 'Delta':
                    value = norm.cdf(d1) -1
                elif ar == 'Gamma':
                    value = norm.pdf(d1) / (p * sigma * np.sqrt(t))
                elif ar == 'Theta':
                    value = (p * norm.pdf(d1) * sigma / 2 * np.sqrt(t)) + (r * K * np.exp(-r * t) * norm.cdf(-d2))
                elif ar == 'Vega':
                    value = p * np.sqrt(t) * norm.pdf(d1)
                row.append(value)
            matrix.append(row)


        df = pd.DataFrame(matrix, index = p10, columns = v10)

        df.index.name = 'Underlying Prices'
        df.columns.name = 'Implied Volatility (%)'
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(df, annot=True,fmt=".3f",ax =ax)
        
        if ar == 'Delta':
            ax.set_title('Delta Put Sensitivity Matrix')
        elif ar == 'Gamma':
            ax.set_title('Gamma Put Sensitivity Matrix')
        elif ar == 'Theta':
            ax.set_title('Theta Put Sensitivity Matrix')
        elif ar == 'Vega':
            ax.set_title('Vega Put Sensitivity Matrix')

        return fig
    except ValueError:
        pass
