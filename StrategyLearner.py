""""""
"""  		  	   		  		 			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
from indicators import *
import pandas as pd
import util as ut
import BagLearner as bl
import RTLearner as rt


class StrategyLearner(object):
    """  		  	   		  		 			  		 			     			  	 
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
        If verbose = False your code should not generate ANY output.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    """
    # constructor
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """  		  	   		  		 			  		 			     			  	 
        Constructor method  		  	   		  		 			  		 			     			  	 
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={'leaf_size': 5}, bags = 20, boost = False)

    # this method should create a QLearner, and train it for trading
    def add_evidence(
        self,
        symbol="IBM",
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 1, 1),
        sv=10000,
    ):
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
        lookback_days = 5
        YBUY = 0.035 + self.impact
        YSELL = -0.035 - self.impact
        upper_band, lower_band = bollinger_band(prices)
        bbp_vals = (prices - lower_band) / (upper_band - lower_band)
        sma_vals = simple_moving_avg(prices)
        macd_vals, macd_signal_vals = MACD(prices)

        bbp = pd.DataFrame(data = bbp_vals)
        sma = pd.DataFrame(data = sma_vals)
        macd = pd.DataFrame(data = macd_vals)
        macd_signal = pd.DataFrame(data = macd_signal_vals)

        data_x = pd.concat((bbp, macd, macd_signal, sma), axis = 1)
        data_x.columns = ['BBP', 'MACD', 'MACD_S', 'SMA']
        data_x['BBP'] = data_x['BBP'].replace(np.nan, 0)
        data_x['SMA'] = data_x['SMA'].replace(np.nan, 0)
        data_x = data_x[:-lookback_days].values
        data_y = np.zeros(data_x.shape[0])
        day_ret = (prices.values[lookback_days:]/prices.values[:-lookback_days]) - 1
        for i in range(data_y.shape[0]):
            if day_ret[i] > YBUY:
                data_y[i] = 1
            elif day_ret[i] < YSELL:
                data_y[i] = -1
            else:
                data_y[i] = 0
        self.learner.add_evidence(data_x, data_y)

        #if self.verbose:
            #print(prices)

        # example use with new colname
        #volume_all = ut.get_data(
            #syms, dates, colname="Volume")  # automatically adds SPY
        #volume = volume_all[syms]  # only portfolio symbols
        #volume_SPY = volume_all["SPY"]  # only SPY, for comparison later
        #if self.verbose:
            #print(volume)

    # this method should use the existing policy and test it against new data
    def testPolicy(
        self,
        symbol="IBM",
        sd=dt.datetime(2009, 1, 1),
        ed=dt.datetime(2010, 1, 1),
        sv=10000,
    ):
        # here we build a fake set of trades
        # your code should return the same sort of data
        # only SPY, for comparison later
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
        trades = prices.copy()
        trades[symbol] = np.zeros(prices.shape[0])
        lookback_window = 5
        upper_band, lower_band = bollinger_band(prices)
        bbp_vals = (prices - lower_band) / (upper_band - lower_band)
        sma_vals = simple_moving_avg(prices)
        macd_vals, macd_signal_vals = MACD(prices)

        bbp = pd.DataFrame(data=bbp_vals)
        sma = pd.DataFrame(data=sma_vals)
        macd = pd.DataFrame(data=macd_vals)
        macd_signal = pd.DataFrame(data=macd_signal_vals)
        data_x = pd.concat((bbp, macd, macd_signal, sma), axis=1)
        data_x.columns = ['BBP', 'MACD', 'MACD_S', 'SMA']
        data_x['BBP'] = data_x['BBP'].replace(np.nan, 0)
        data_x['SMA'] = data_x['SMA'].replace(np.nan, 0)
        test_x = data_x[:-lookback_window].values
        test_y = self.learner.query(test_x)
        signal = 0
        shares = 0
        for i in range(test_y.shape[0]):
            if test_y[i] > 0:
                signal = 1
            elif test_y[i] < 0:
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

    def author(self):
        return "vpatel436"

if __name__ == "__main__":
    print("One does not simply think up a strategy")
    sl = StrategyLearner()
    sl.add_evidence(symbol="IBM",sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009, 1, 1),sv=10000)
    sl.testPolicy(symbol="IBM",sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009, 1, 1),sv=10000)
