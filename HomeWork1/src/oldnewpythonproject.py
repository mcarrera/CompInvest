import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd



def simulate(startdate, enddate, symbols, weights):

    startdate = dt_start 
    enddate = dt_end
    symbols = ls_symbols
    weights= ls_alloc


    # get the data 
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    #normalize
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]

    #returns
    na_rets = na_price.copy()
    tsu.returnize0(na_rets)
    last_day = len(na_price) - 1
    cumulative_return = np.sum(weights * (na_price[last_day]/na_price[0] - 1.0))
 
    #average daily return
    avg_daily_return = (np.sum(cumulative_return) / 252)
 
    #volatility
    volatility = (np.std(np.sum(na_rets * weights, axis=1)))
    
    # sharpe ratio
    #( average_daily_return/standard_deviation_of_daily_returns ) * sqrt(252)
    sharpe_ratio =  ((np.sum(cumulative_return) / 252.0) / volatility) * np.sqrt(252    )
    
    return volatility, avg_daily_return, sharpe_ratio, cumulative_return
    
    


ls_symbols = ['BRCM', 'TXN', 'AMD', 'ADI'] 
ls_alloc = [0.4, 0.4, 0.0, 0.2]
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, ls_alloc)

print("Start Date: " + str(dt_start))
print("End Date: " + str(dt_end))
print("Symbols: " + str(ls_symbols))
print("Optimal Allocation: " + str(ls_alloc))
print("Sharpe Ratio: " + str(sharpe))
print("Volatility (stdev of daily returns): " + str(vol))
print("Average Daily Return: " + str(daily_ret))
print("Cumulative Return: " + str(cum_ret))
