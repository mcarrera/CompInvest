import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
def simulate(startdate, enddate, symbols, weights, data):

    startdate = dt_start 
    enddate = dt_end
    symbols = ls_symbols
    d_data = data

    #normalize
    na_price = d_data['close'].values
   
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

# init
ls_symbols =    ['C', 'GS', 'IBM', 'HNZ'] 
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
max_sharp_ratio = -99990.0
best_portfolio = [0.0, 0.0, 0.0, 0.0]

# get the data 
dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
ls_keys = ['close']
ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))

# mumbo jumbo
NumberofEquity = len(ls_symbols)
delta = 0.10;
incrArray=[0.0 + i * delta for i in range(0,11)]
operations = (len(incrArray))**NumberofEquity - 1
arrangement = [incrArray[0] for i in range(0,NumberofEquity)]

pos = NumberofEquity-1;
maxminusone=incrArray[len(incrArray)-2]+delta/2.0;
maxplusone=incrArray[len(incrArray)-1]+delta-delta/2.0;

increments = 0;
while increments < operations:
	if arrangement[pos] > maxminusone:
		arrangement[pos] = incrArray[0]
		pos-=1
	else:
		arrangement[pos]+=delta;
		increments+=1
		pos=NumberofEquity-1
		norm = np.sum(arrangement)
		if (norm > maxminusone and norm < maxplusone):
#			print arrangement, np.sum(arrangement)
                        vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, arrangement, d_data)
#                        print("Sharpe Ratio: " + str(sharpe))
			if(sharpe > max_sharp_ratio):
                            max_sharp_ratio = sharpe
                            best_portfolio = np.copy(arrangement)

print("Max Sharpe Ratio: " + str(max_sharp_ratio))
print(best_portfolio)