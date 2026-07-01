import numpy as np
import streamlit as st
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import inspect
from markets import convert
from markets import marketcall
import seaborn as sns
from markets import marketput
from greeks import matrixcall
from greeks import matrixput
import matplotlib.pyplot as plt


# front page

st.header('Black-Scholes Options Price Simulator', divider = 'blue')
st.latex(r'C(S,t) = N(d_1)S - N(d_2)K e^{-rt}')
st.latex(r'd_1 = \frac{\ln(\frac{S}{K}) + (r + \frac{\sigma^2}{2})t}{\sigma \sqrt{t}} ')
st.latex(r'd_2 = d_1 - \sigma\sqrt{t}')






def main():
    with st.sidebar:
        mysidebar = st.radio('Real Markets or Own Parameters', ['Markets', 'Own Parameters'])
    if mysidebar == 'Markets':
        markets()
    else:
        myown()
    

def markets():
    try:
        with st.sidebar:
            marketcallput = st.radio("Choose which type of option you would like to purchase", ['Call', 'Put'])
            tick = st.text_input("Ticker: ")
            if tick == '':
                raise ValueError()
        data = convert(tick, marketcallput)
    except ValueError:
        pass
    else:
        marketoutput(data)
        
        
def marketoutput(data):
   st.write(data[['lastTradeDate','strike','impliedVolatility','lastPrice']])
   

def myown():
    global calc

    try:
        with st.sidebar:
            st.header("Parmeters")
            selected = st.radio('Choose which type of option you would like to purchase', ['Call', 'Put'])
            stockprice = st.number_input("Stock Price: ",min_value=0, value=0, step=1)
            strikeprice = st.number_input("Strike: ",min_value=0, value=0, step=1)
            riskfreerate = st.slider('Risk-Free Interest Rate: ',min_value=0.0, max_value=0.50, value=0.04, step=0.01)
            volatility = st.slider('Implied Volatility (%)', min_value = 1, value = 1, step = 1)
            timetoexpiration = st.number_input("Days to Expiration: ",min_value=0, value=0, step=1)
            calc = st.button("Calculate Option Price")
            
                
        
            
        if calc:
            if selected == 'Call':
                call(stockprice,strikeprice,riskfreerate,volatility / 100,timetoexpiration)
            else:
                put(stockprice,strikeprice,riskfreerate,volatility / 100,timetoexpiration)
        if stockprice > 0 and strikeprice > 0 and volatility > 0 and timetoexpiration > 0:
            if selected == 'Call':
                greekcall(stockprice,strikeprice,riskfreerate,volatility / 100,timetoexpiration)
            else:
                greekput(stockprice,strikeprice,riskfreerate,volatility / 100,timetoexpiration)
                
            
        
    except ZeroDivisionError:
        pass        


def call(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    d2 = d1 - sigma * np.sqrt(t/365)
    black = S__t * norm.cdf(d1) - K * np.exp(-r * (t/365)) * norm.cdf(d2)
    output(black)
    

def put(S__t, K, r, sigma, t):
    d1 = (np.log(S__t / K) + (r + (sigma**2 / 2)) * (t/365)) / (sigma * np.sqrt(t/365))
    d2 = d1 - sigma * np.sqrt(t/365)
    black = K * np.exp(-r*(t/365)) * norm.cdf(-d2) - S__t * norm.cdf(-d1)
    output(black)

def output(n):
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    if caller_name == 'call':
        st.subheader('Call Option Premium')
        st.success(n)
    elif caller_name == 'put':
        st.subheader('Put Option Premium')
        st.success(n)
        
def greekcall(S__t, K, r, sigma, t):
    with st.sidebar:
        gr = st.segmented_control("What Option Greek Matrix do you want displayed" , ['Delta','Gamma','Theta','Vega'], default = 'Delta')
        data = matrixcall(gr, S__t, K, r, sigma, t)
    matcall(gr, S__t, K, r, sigma, t)
    
    st.write(data)

def greekput(S__t, K, r, sigma, t):
    with st.sidebar:
        ar = st.segmented_control("What Option Greek Matrix do you want displayed" , ['Delta','Gamma','Theta','Vega'], default = 'Delta')
        data = matrixput(ar, S__t, K, r, sigma, t)
    matput(ar, S__t, K, r, sigma, t)
    st.write(data)
    
    
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
        st.pyplot(fig)
        
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

        st.pyplot(fig)
    except ValueError:
        pass





# whenever you want to update your code in github do these commadnds in the terminal
git add .
git commit -m "Update app"
git push

if __name__ == "__main__":
    main()