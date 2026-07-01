import numpy as np
import streamlit as st
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import inspect

from markets import convert
from greeks import matrixcall
from greeks import matrixput
from matrix import matcall
from matrix import matput



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
        fig = matcall(gr, S__t, K, r, sigma, t)
    st.write(data)
    st.pyplot(fig)

def greekput(S__t, K, r, sigma, t):
    with st.sidebar:
        ar = st.segmented_control("What Option Greek Matrix do you want displayed" , ['Delta','Gamma','Theta','Vega'], default = 'Delta')
        data = matrixput(ar, S__t, K, r, sigma, t)
        fig = matput(ar, S__t, K, r, sigma, t)
    st.write(data)
    st.pyplot(fig)
    






# whenever you want to update your code in github do these commadnds in the terminal
#git add .
#git commit -m "Update app"
#git push

if __name__ == "__main__":
    main()