import pandas as pd
import yfinance as yf
import numpy as np
import json as js
import matplotlib.pyplot as plt
dat = yf.Ticker("TSLA")

history=dat.history(period="2y", interval="1d")
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

short_window = 20
long_window = 50

history["MA_short"] = history["Close"].rolling(window=short_window).mean()
history["MA_long"] = history["Close"].rolling(window=long_window).mean()


signal_list = []
prev_signal = 0

for date in dates:
    ma_short = history["MA_short"][date]
    ma_long = history["MA_long"][date]
    if pd.isna(ma_short) or pd.isna(ma_long):
        current_signal = 0
    elif ma_short > ma_long:
        current_signal = 1
    elif ma_short < ma_long:
        current_signal = -1
    else:
        current_signal = 0

    signal_list.append(current_signal)

history["Signal"] = signal_list

position_list = []
buy_dates = []
sell_dates = []
buy_prices = []
sell_prices = []

prev_signal = None

for date in dates:
    current_signal = history["Signal"][date]

    if prev_signal is None:
        position = None
    else:
        position = current_signal - prev_signal

    position_list.append(position)

    if position == 2:
        buy_dates.append(date)
        buy_prices.append(history["Close"][date])

    if position == -2:
        sell_dates.append(date)
        sell_prices.append(history["Close"][date])

    prev_signal = current_signal

history["Position"] = position_list



history["SMA_20"]=history["Close"].rolling(20).mean()
history["SMA_50"]=history["Close"].rolling(50).mean()

plt.figure(figsize = (10,10))
plt.plot(history["SMA_20"])
plt.plot(history["SMA_50"])
plt.plot(history["Close"])
plt.legend(["SMA_20", "SMA_50", "Close"])
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()