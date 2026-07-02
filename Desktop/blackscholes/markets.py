import yfinance as yf
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from datetime import datetime


class Call:
    def __init__(self, strike, period):
        self.strike = strike
        self.period = int(period)
    
    def marketcall(self, chain):
        calls = chain.calls
        return calls.loc[calls['strike'] >= self.strike]

    def callvolsurf(self, ticker, tick):
        test = ticker.options[:self.period]


        calldf = []

        for date in test:
            try:
                aqr = str(date)
                aqr = aqr.replace('00:00:00','').strip()
                chain = ticker.option_chain(aqr)
                calldf.append(chain.calls)
            except ValueError:
                pass

        dfc = pd.concat(calldf, ignore_index=True)
        maturity = dfc["contractSymbol"]
            
        daysag = []

        for symbol in maturity:
            cleaned = symbol.replace(tick.upper(), "").strip()

            exp_str = cleaned[:6]

            trade_date = datetime.strptime(exp_str, "%y%m%d")
            today_date = datetime.now()

            days_to_maturity = (trade_date - today_date).days

            daysag.append(days_to_maturity)

        dfc["days_to_maturity"] = daysag
        
        return dfc

       
        

class Put:
    def __init__(self, strike, period):
        self.strike = strike
        self.period = int(period)
    
    def marketput(self, chain):
        put = chain.puts
        return put.loc[put['strike'] >= self.strike]
    
    def putvolsurf(self, ticker, tick):
        test = ticker.options[:self.period]

        putdf = []
        for date in test:
            try:
                aqr = str(date)
                aqr = aqr.replace('00:00:00','').strip()
                chain = ticker.option_chain(aqr)
                putdf.append(chain.puts)
            except ValueError:
                pass
            
        dfp = pd.concat(putdf, ignore_index=True)
        maturity = dfp["contractSymbol"]
            
        daysag = []

        for symbol in maturity:
            cleaned = symbol.replace(tick.upper(), "").strip()

            # first 6 chars after ticker = YYMMDD
            exp_str = cleaned[:6]

            trade_date = datetime.strptime(exp_str, "%y%m%d").date()
            today_date = datetime.now()

            days_to_maturity = (trade_date - today_date).days

            daysag.append(days_to_maturity)

        dfp["days_to_maturity"] = daysag
        return dfp


        
        
        


def convert(type, tick, strike, period):
    global chain
    global ticker
    ticker = yf.Ticker(tick)
    expiration = ticker.options[0]
    chain = ticker.option_chain(expiration)
    if type == 'Call':
        call = Call(strike, period)
        marketdata = call.marketcall(chain)
        volsurf = call.callvolsurf(ticker, tick)
        return marketdata, volsurf
    elif type == 'Put':
        put = Put(strike, period)
        marketdata = put.marketput(chain)
        volsurf = put.putvolsurf(ticker, tick)
        return marketdata, volsurf


    
    

    

        
