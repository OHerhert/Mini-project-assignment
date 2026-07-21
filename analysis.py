import pandas as pd
import yfinance as yf
import numpy as np
import json as js
import matplotlib.pyplot as plt
dat = yf.Ticker("TSLA")
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


history["SMA_20"]=history["Close"].rolling(20).mean()
history["SMA_50"]=history["Close"].rolling(50).mean()
plt.figure(figsize = (10,10))
plt.plot(history["SMA_20"])
plt.plot(history["SMA_50"])
plt.plot(history["Close"])
plt.legend(["SMA_20", "SMA_50", "Close"])
plt.xlabel("Days")
plt.ylabel("Price")
plt.show()