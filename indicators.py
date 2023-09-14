import datetime as dt
import numpy as np
import marketsimcode as msc
import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt

def author():
    return "vpatel436"

def bollinger_band(prices):
    window = 20
    prices_rolling = prices.rolling(window)
    prices_sma = prices_rolling.mean()
    prices_std = prices_rolling.std()
    upper_bound = prices_sma + (2 * prices_std)
    lower_bound = prices_sma - (2 * prices_std)
    bollinger_band = (prices - prices_sma) / (2 * prices_std)
    return upper_bound, lower_bound
def simple_moving_avg(prices):
    #norm_prices = prices/prices.iloc[0]
    window = 20
    prices_rolling = prices.rolling(window)
    prices_sma = prices_rolling.mean()
    sma_ratio = prices/prices_sma
    return sma_ratio

def MACD(prices):
    short_window = 12
    long_window = 26
    signal_window = 9
    short_ema = prices.ewm(span = short_window, adjust = False).mean()
    long_ema = prices.ewm(span = long_window, adjust = False).mean()
    macd = short_ema - long_ema
    macd_signal = macd.ewm(span = signal_window, adjust = False).mean()
    return macd, macd_signal

def momentum(prices):
    window = 20
    norm_prices = prices/prices.iloc[0]
    momentum = (norm_prices / norm_prices.shift(window)) - 1
    return momentum

def stochastic_oscillator(prices):
    k_window = 14
    d_window = 3
    lowest = prices.rolling(window = k_window, center= False).min()
    highest = prices.rolling(window = k_window, center= False).max()
    percent_k = (prices - lowest)/(highest - lowest) * 100
    percent_d = percent_k.rolling(window= d_window).mean()
    return percent_d
def test_code():
    symbol = ['JPM']
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    prices_all = get_data(symbol, dates)
    prices = prices_all[symbol]
    simple_moving_avg(prices)
    bollinger_band(prices)
    momentum(prices)
    MACD(prices)
    stochastic_oscillator(prices)