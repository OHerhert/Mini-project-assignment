import pandas as pd
import yfinance as yf
import numpy as np
import json as js
dat = yf.Ticker("TSLA")
dat.info
dat.calendar
dat.analyst_price_targets
dat.quarterly_income_stmt
dat.option_chain(dat.options[0]).calls
dat.quarterly_income_stmt.to_csv("quarterly_income_stmt.csv")
history=dat.history(period="1y", interval="1d")
history.to_csv("Historical data")

hist_data={}
dates=history.index
for data in dates:
    date=str(data)[:10]
    hist_data[date]={
        "Open":float(history["Open"][data]),
        "Close":float(history["Close"][data]),
        "High":float(history["High"][data]),
        "Low":float(history["Low"][data]),
        "Volume":int(history["Volume"][data])
    }
with open("history.json", "w") as file:
    js.dump(hist_data, file, indent=4)


