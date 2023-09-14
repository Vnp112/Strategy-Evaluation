import datetime as dt
import numpy as np
import marketsimcode as msc
import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt
from indicators import *

def testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000):
    sym = [symbol]
    dates = pd.date_range(sd, ed)
    price = get_data(sym, dates)
    price = price.ffill().bfill()
    price = price[sym]
    trades = price.copy()
    trades[symbol] = np.zeros(price.shape[0])
    shares = 0
    signal = 0
    plt.figure(figsize=(10, 8))
    plt.grid()
    bollinger_upper_band, bollinger_lower_band = bollinger_band(price)
    bbp = (price - bollinger_lower_band) / (bollinger_upper_band - bollinger_lower_band)
    simple_moving_avg_val = simple_moving_avg(price)
    macd_val, macd_signal_val = MACD(price)
    for i in range(price.shape[0]-1):
        curr_macd = macd_val[symbol].iloc[i]
        curr_macd_signal = macd_signal_val[symbol].iloc[i]
        curr_bbp = bbp[symbol].iloc[i]
        curr_sma = simple_moving_avg_val[symbol].iloc[i]
        if curr_sma < 0.975:
            if curr_macd > curr_macd_signal + 0.05 or curr_bbp < 0.2:
                signal = 1
        elif curr_sma > 1.025:
            if curr_macd < curr_macd_signal - 0.05 or curr_bbp > 0.8:
                signal = -1
        else:
            signal = 0

        if signal == 1:
            if shares == 0:
                shares += 1000
                trades.iloc[i] = 1000
            elif shares == -1000:
                shares += 2000
                trades.iloc[i] = 2000
            else:
                trades.iloc[i] = 0

        elif signal == -1:
            if shares == 1000:
                shares -= 2000
                trades.iloc[i] = -2000
            elif shares == 0:
                shares -= 1000
                trades.iloc[i] = -1000
            else:
                trades.iloc[i] = 0
        else:
            trades.iloc[i] = 0
    return trades

def benchmark_trades(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
    sym = [symbol]
    dates = pd.date_range(sd, ed)
    price = get_data(sym, dates)
    price = price.ffill().bfill()
    price = price[sym]
    benchmark = price.copy()
    benchmark[symbol] = np.zeros(benchmark.shape[0])
    benchmark.iloc[0][symbol] = 1000
    return benchmark

def port_stats(trades_portvals):
    trades_cum_ret = (trades_portvals[-1]/trades_portvals[0]) - 1
    trades_daily_ret = (trades_portvals/trades_portvals.shift(1)) - 1
    trades_daily_ret = trades_daily_ret[1:]
    trades_avg_daily_ret = trades_daily_ret.mean()
    trades_std_daily_ret = trades_daily_ret.std()

    return trades_cum_ret, trades_avg_daily_ret, trades_std_daily_ret

def author():
    return "vpatel436"

def test_code():
    symbol = 'JPM'
    in_sample_trades = testPolicy(symbol=symbol , sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    in_sample_benchmark = benchmark_trades(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    in_sample_trades_portvals = msc.compute_portvals(in_sample_trades, start_val=100000, commission=9.95, impact=0.005)
    in_sample_benchmark_portvals = msc.compute_portvals(in_sample_benchmark, start_val=100000, commission=9.95, impact=0.005)
    normed_in_sample_trades_portvals = in_sample_trades_portvals/in_sample_trades_portvals.iloc[0]
    normed_in_sample_benchmark_portvals = in_sample_benchmark_portvals/in_sample_benchmark_portvals.iloc[0]
    print("In-Sample Manual Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(port_stats(in_sample_trades_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(port_stats(in_sample_trades_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(port_stats(in_sample_trades_portvals)[2])}")
    print("-----------------------------------------------")
    print("In-Sample Benchmark Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(port_stats(in_sample_benchmark_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(port_stats(in_sample_benchmark_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(port_stats(in_sample_benchmark_portvals)[2])}\n")
    plt.title("Manual Strategy vs Benchmark for JPM (In-Sample)")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Values")
    plt.plot(normed_in_sample_benchmark_portvals, label = 'Benchmark', color = 'purple')
    plt.plot(normed_in_sample_trades_portvals, label = 'Manual', color = 'red')
    for i in range(in_sample_trades.shape[0]-1):
        if in_sample_trades[symbol].iloc[i] > 0:
            plt.axvline(x=in_sample_trades.index.tolist()[i], color='blue')
        elif in_sample_trades[symbol].iloc[i] < 0:
            plt.axvline(x=in_sample_trades.index.tolist()[i], color='black')
    plt.legend(loc = 'upper left')
    plt.savefig('In_Sample')
    plt.clf()

    out_sample_trades = testPolicy(symbol=symbol, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    out_sample_benchmark = benchmark_trades(symbol=symbol, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31),sv=100000)
    out_sample_trades_portvals = msc.compute_portvals(out_sample_trades, start_val=100000, commission=9.95, impact=0.005)
    out_sample_benchmark_portvals = msc.compute_portvals(out_sample_benchmark, start_val=100000, commission=9.95, impact=0.005)
    normed_out_sample_trades_portvals = out_sample_trades_portvals / out_sample_trades_portvals.iloc[0]
    normed_out_sample_benchmark_portvals = out_sample_benchmark_portvals / out_sample_benchmark_portvals.iloc[0]
    print("Out-of-Sample Manual Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(port_stats(out_sample_trades_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(port_stats(out_sample_trades_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(port_stats(out_sample_trades_portvals)[2])}")
    print("-----------------------------------------------")
    print("Out-of-Sample Benchmark Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(port_stats(out_sample_benchmark_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(port_stats(out_sample_benchmark_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(port_stats(out_sample_benchmark_portvals)[2])}\n")
    plt.title("Manual Strategy vs Benchmark for JPM (Out-of-Sample)")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Values")
    plt.plot(normed_out_sample_benchmark_portvals, label = 'Benchmark', color = 'purple')
    plt.plot(normed_out_sample_trades_portvals, label = 'Manual', color = 'red')
    for i in range(out_sample_trades.shape[0]-1):
        if out_sample_trades[symbol].iloc[i] > 0:
            plt.axvline(x=out_sample_trades.index.tolist()[i], color='blue')
        elif in_sample_trades[symbol].iloc[i] < 0:
            plt.axvline(x=out_sample_trades.index.tolist()[i], color='black')
    plt.legend(loc = 'upper left')
    plt.savefig('Out_Sample')
    plt.clf()
