""""""
"""MC2-P1: Market simulator.  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
Student Name: Vasu Patel (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: vpatel436 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 903850596 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""

import datetime as dt
import os
import math
import numpy as np
import pandas as pd
from util import get_data, plot_data

def compute_portvals(
        trades_df,
        start_val=1000000,
        commission=9.95,
        impact=0.005,
):
    trades_df = trades_df.sort_index()
    sd = trades_df.index[0]  # get start date
    ed = trades_df.index[-1]  # get end date
    dates = pd.date_range(sd, ed)
    sym = trades_df.columns[0]
    prices = get_data([sym], dates)
    prices = prices.drop(['SPY'], axis=1)
    prices['CASH'] = np.ones(prices.shape[0])
    day_trades = prices.copy()
    day_trades.iloc[:] = 0
    day_trades['CASH'] = np.zeros(trades_df.shape[0])
    trade_rows = trades_df.iterrows()

    for index, row in trade_rows:
        if row[sym] > 0:
            day_trades.at[index, sym] += row[sym]
            sym_price = prices.at[index, sym]
            buy_price = row[sym] * sym_price * (1 + impact) + commission
            day_trades.at[index, 'CASH'] -= buy_price
        elif row[sym] < 0:
            day_trades.at[index, sym] += row[sym]
            sym_price = prices.at[index, sym]
            sell_price = -row[sym] * sym_price * (1 - impact) - commission
            day_trades.at[index, 'CASH'] += sell_price
        elif row[sym] == 0:
            continue

    holdings = day_trades.copy()
    holdings.iloc[0]['CASH'] += start_val
    for i in range(1, len(holdings)):
        holdings.iloc[i] = holdings.iloc[i - 1] + holdings.iloc[i]
    holdings = prices * holdings
    holdings['Values'] = holdings.sum(axis=1)
    portvals = holdings['Values']
    return portvals

def author():
    return "vpatel436"

if __name__ == "__main__":
    print('test')