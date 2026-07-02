import yfinance as yf
from datetime import date, timedelta
import sys
import pandas as pd

ticker = yf.Ticker("AAPL")



inp = inp
test = ticker.options[:inp]


calldf = []
putdf = []
for date in test:
    try:
        aqr = str(date)
        aqr = aqr.replace('00:00:00','').strip()
        chain = ticker.option_chain(aqr)
        calldf.append(chain.calls)
        putdf.append(chain.puts)
    except ValueError:
        pass

dfc = pd.concat(calldf)
dfp = pd.concat(putdf)

print(dfc)

        
    

    
    
    
sys.exit()

chain = ticker.option_chain()
sys.exit()

sys.exit()








calls = chain.calls
puts = chain.puts


print("Using expiration:", expiration)
print(calls[["contractSymbol", "strike", "bid", "ask", "impliedVolatility"]])