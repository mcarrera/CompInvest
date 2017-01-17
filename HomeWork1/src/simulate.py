import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd



def simulate(startdate, enddate, symbols, weights):
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
    na_port_value = np.sum(na_normalized_price * weights, axis=1)
    
    na_port_rets = na_port_value.copy()
    tsu.returnize0(na_port_rets)
   
    #volatility  (stdev of daily returns)
    volatility = np.std(na_port_rets) # good! 0.0101467067654
    
    
    #returns
    cumulative_return = np.prod(na_port_rets + 1) #good! 1.16487261965
    avg_daily_return = np.average(na_port_rets) #good  0.000657261102001
      
    # sharpe ratio
    #( average_daily_return/standard_deviation_of_daily_returns ) * sqrt(252)
    sharpe_ratio =  (avg_daily_return  / volatility) * np.sqrt(252)  #good! 1.02828403099
    
    return volatility, avg_daily_return, sharpe_ratio, cumulative_return
    #return
    


ls_symbols =  ['BRCM', 'ADBE', 'AMD', 'ADI'] 
ls_alloc = [0.0, 0.0, 0.1, 0.9]
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
simulate(dt_start, dt_end, ls_symbols, ls_alloc)
vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, ls_alloc)

print("Start Date: " + str(dt_start))
print("End Date: " + str(dt_end))
print("Symbols: " + str(ls_symbols))
print("Optimal Allocation: " + str(ls_alloc))
print("Sharpe Ratio: " + str(sharpe))
print("Volatility (stdev of daily returns): " + str(vol))
print("Average Daily Return: " + str(daily_ret))
print("Cumulative Return: " + str(cum_ret))
