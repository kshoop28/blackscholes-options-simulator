import yfinance as yf
import pandas as pd
import numpy as np
import time


def convert(n, a):
    global chain
    ticker = yf.Ticker(n)
    expiration = ticker.options[0]
    chain = ticker.option_chain(expiration)
    if a == 'Call':
        return marketcall(ticker)
    else:
        return marketput(ticker)
    
def marketcall(n):
    calls = chain.calls
    return calls
    
    
def marketput(n):
    puts = chain.puts
    return puts    
    

        
