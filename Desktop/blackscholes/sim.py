import numpy as np
import streamlit as st
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import inspect
from datetime import datetime
from matplotlib import projections
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


import plotly.graph_objects as go


from markets import convert
from greeks import matrixcall
from greeks import matrixput
from greeksmatrix import matcall
from greeksmatrix import matput



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
    global tick
    try: 
        with st.sidebar:
            marketcallput = st.radio("Choose which type of option you would like to purchase", ['Call', 'Put'])
            tick = st.text_input("Ticker: ")
        
            strike_input = st.text_input("Minimum Strike:", value="100")
            

            strike = float(strike_input)
            
            
            date_input = st.text_input("Number of expiration dates to include", value = 1)
            
            if date_input == None:
                raise ValueError()
            
            if strike == None:
                raise ValueError()
            
            
    

            if tick == '':
                raise ValueError()
            
    except ValueError:
        st.write("")
        
    else:
        market_data, vol_surface = convert(marketcallput, tick, strike, date_input)

        marketoutput(market_data)
        createsurf(vol_surface)
    

def createsurf(volsurf):
    df = volsurf.copy()

    df = df.dropna(subset=['strike', 'days_to_maturity', 'impliedVolatility'])

    df = df[
        (df['impliedVolatility'] > 0) &
        (df['impliedVolatility'] < 2) &
        (df['days_to_maturity'] > 0)
    ]

    low = df['strike'].quantile(0.05)
    high = df['strike'].quantile(0.95)
    df = df[df['strike'].between(low, high)]

    surface_df = df.pivot_table(
        index='days_to_maturity',
        columns='strike',
        values='impliedVolatility',
        aggfunc='mean'
    )

    fig = go.Figure(data=[
        go.Surface(
            x=surface_df.columns,
            y=surface_df.index,
            z=surface_df.values,
            connectgaps = True
        )
    ])

    fig.update_layout(
        title='Volatility Surface',
        scene=dict(
            xaxis_title='Strike',
            yaxis_title='Days to Maturity',
            zaxis_title='Implied Volatility'
            
        ),
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)

def marketoutput(data):
    try:
        if data.empty:
            raise TypeError()
        st.write(data[['lastTradeDate','strike','impliedVolatility','lastPrice']])
    except TypeError:
        st.write(f'No options were purchased with that strike today')
        


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