import datetime as dt
import matplotlib.pyplot as plt
import ManualStrategy as ms
import StrategyLearner as sl
import marketsimcode as msc

def author():
    return "vpatel436"

def exp2():
    strategy_learner_1 = sl.StrategyLearner(verbose=False, impact=0.00, commission=0.0)
    strategy_learner_2 = sl.StrategyLearner(verbose=False, impact=0.08, commission=0.0)
    strategy_learner_3 = sl.StrategyLearner(verbose=False, impact=0.15, commission=0.0)

    strategy_learner_1.add_evidence(symbol= "JPM", sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sv=100000)
    strategy_learner_2.add_evidence(symbol= "JPM", sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sv=100000)
    strategy_learner_3.add_evidence(symbol= "JPM", sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sv=100000)

    sl1_trades = strategy_learner_1.testPolicy(symbol= "JPM", sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sv=100000)
    sl2_trades = strategy_learner_2.testPolicy(symbol= "JPM", sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sv=100000)
    sl3_trades = strategy_learner_3.testPolicy(symbol= "JPM", sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), sv=100000)

    sl1_portvals = msc.compute_portvals(sl1_trades, start_val=100000, commission=0.0, impact=0.005)
    sl2_portvals = msc.compute_portvals(sl2_trades, start_val=100000, commission=0.0, impact=0.005)
    sl3_portvals = msc.compute_portvals(sl3_trades, start_val=100000, commission=0.0, impact=0.005)

    normed_sl1_portvals = sl1_portvals / sl1_portvals.iloc[0]
    normed_sl2_portvals = sl2_portvals / sl2_portvals.iloc[0]
    normed_sl3_portvals = sl3_portvals / sl3_portvals.iloc[0]

    plt.figure(figsize=(10,8))
    plt.grid()
    plt.title("Strategy Learner Portfolio Values of Varying Impact Values")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Values")
    plt.plot(normed_sl1_portvals, label = 'Impact = {}'.format(strategy_learner_1.impact), color = 'red')
    plt.plot(normed_sl2_portvals, label='Impact = {}'.format(strategy_learner_2.impact), color='green')
    plt.plot(normed_sl3_portvals, label='Impact = {}'.format(strategy_learner_3.impact), color='blue')
    plt.legend()
    plt.savefig('Experiment 2-1')
    plt.clf()

    plt.figure()
    impacts = ['{}'.format(strategy_learner_1.impact), '{}'.format(strategy_learner_2.impact), '{}'.format(strategy_learner_3.impact)]
    trade_counts = [trade_count(sl1_trades, 'JPM'), trade_count(sl2_trades, 'JPM'), trade_count(sl3_trades, 'JPM')]
    plt.bar(impacts, trade_counts)
    plt.xlabel('Impact')
    plt.ylabel('Number of Trades')
    plt.title('Strategy Learner Impact vs. Trade Count')
    plt.savefig('Experiment 2-2')

def trade_count(trades, symbol):
    count = 0
    for i in range(trades.shape[0]):
        if trades[symbol].iloc[i] > 0 or trades[symbol].iloc[i] < 0:
            count += 1
    return count

def test_code():
    exp2()