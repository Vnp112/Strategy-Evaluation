import datetime as dt
import matplotlib.pyplot as plt
import ManualStrategy as ms
import StrategyLearner as sl
import marketsimcode as msc
def author():
    return "vpatel436"

def exp1():
    manual_learner = ms
    in_strategy_learner = sl.StrategyLearner(verbose = False, impact = 0.0, commission=0.0)
    in_strategy_learner.add_evidence(symbol="JPM",sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009, 12, 31),sv=100000)

    in_strategy_trades = in_strategy_learner.testPolicy(symbol="JPM",sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009, 12, 31),sv=100000)
    in_manual_trades = manual_learner.testPolicy(symbol="JPM",sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009, 12, 31),sv=100000)
    in_benchmark_trades = manual_learner.benchmark_trades(symbol="JPM",sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009, 12, 31),sv=100000)

    in_strategy_portvals = msc.compute_portvals(in_strategy_trades, start_val=100000, commission=9.95, impact=0.005)
    in_manual_portvals = msc.compute_portvals(in_manual_trades, start_val=100000, commission=9.95, impact=0.005)
    in_benchmark_portvals = msc.compute_portvals(in_benchmark_trades, start_val =100000, commission=9.95, impact=0.005)

    normed_in_strategy_portvals = in_strategy_portvals/in_strategy_portvals.iloc[0]
    normed_in_manual_portvals = in_manual_portvals/in_manual_portvals.iloc[0]
    normed_in_benchmark_portvals = in_benchmark_portvals/in_benchmark_portvals.iloc[0]

    print("Experiment 1 Statistics:")
    print("In-Sample Manual Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(ms.port_stats(in_manual_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(ms.port_stats(in_manual_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(ms.port_stats(in_manual_portvals)[2])}")
    print("-----------------------------------------------")
    print("In-Sample Benchmark Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(ms.port_stats(in_benchmark_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(ms.port_stats(in_benchmark_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(ms.port_stats(in_benchmark_portvals)[2])}")
    print("-----------------------------------------------")
    print("In-Sample Strategy Learner Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(ms.port_stats(in_strategy_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(ms.port_stats(in_strategy_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(ms.port_stats(in_strategy_portvals)[2])}")
    print("-----------------------------------------------")

    plt.title("Manual Strategy vs Strategy Learner vs Benchmark for JPM (In-Sample)")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Values")
    plt.plot(normed_in_strategy_portvals, label='Strategy', color='purple')
    plt.plot(normed_in_manual_portvals, label='Manual', color='red')
    plt.plot(normed_in_benchmark_portvals, label='Benchmark', color='green')
    plt.legend(loc='upper left')
    plt.savefig('Experiment 1 - In Sample')
    plt.clf()

    out_strategy_learner = sl.StrategyLearner()
    out_strategy_learner.add_evidence(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)

    out_strategy_trades = out_strategy_learner.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    out_manual_trades = manual_learner.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    out_benchmark_trades = manual_learner.benchmark_trades(symbol="JPM",sd=dt.datetime(2010, 1, 1),ed=dt.datetime(2011, 12, 31),sv=100000)

    out_strategy_portvals = msc.compute_portvals(out_strategy_trades, start_val=100000, commission=9.95, impact=0.005)
    out_manual_portvals = msc.compute_portvals(out_manual_trades, start_val=100000, commission=9.95, impact=0.005)
    out_benchmark_portvals = msc.compute_portvals(out_benchmark_trades, start_val=100000, commission=9.95, impact=0.005)

    normed_out_strategy_portvals = out_strategy_portvals / out_strategy_portvals.iloc[0]
    normed_out_manual_portvals = out_manual_portvals / out_manual_portvals.iloc[0]
    normed_out_benchmark_portvals = out_benchmark_portvals / out_benchmark_portvals.iloc[0]

    print("Out-of-Sample Manual Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(ms.port_stats(out_manual_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(ms.port_stats(out_manual_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(ms.port_stats(out_manual_portvals)[2])}")
    print("-----------------------------------------------")
    print("Out-of-Sample Benchmark Strategy Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(ms.port_stats(out_benchmark_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(ms.port_stats(out_benchmark_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(ms.port_stats(out_benchmark_portvals)[2])}")
    print("-----------------------------------------------")
    print("Out-of-Sample Strategy Learner Stats:")
    print(f"Cumulative Return: {'{:.6f}'.format(ms.port_stats(out_strategy_portvals)[0])}")
    print(f"Average Daily Return: {'{:.6f}'.format(ms.port_stats(out_strategy_portvals)[1])}")
    print(f"Standard Deviation of Daily Return: {'{:.6f}'.format(ms.port_stats(out_strategy_portvals)[2])}\n")

    plt.title("Manual Strategy vs Strategy Learner vs Benchmark for JPM (Out-of-Sample)")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Portfolio Values")
    plt.plot(normed_out_strategy_portvals, label='Strategy', color='purple')
    plt.plot(normed_out_manual_portvals, label='Manual', color='red')
    plt.plot(normed_out_benchmark_portvals, label='Benchmark', color='green')
    plt.legend(loc='upper left')
    plt.savefig('Experiment 1 - Out Sample')
    plt.clf()
def test_code():
    exp1()