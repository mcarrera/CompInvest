import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu

if __name__ == '__main__':
    print "Start"
    #setup
    lookback = 20
    dt_start = dt.datetime(2008, 1,1)
    dt_end = dt.datetime(2009, 12, 31) 
    ldt_timestamps = du.getNYSEdays(dt_start  - dt.timedelta(lookback*3), dt_end, dt.timedelta(hours=16))
    ls_timestamps = []
    
    # get data
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = ['AAPL', 'MSFT']
    ls_keys = ['actual_close']
    df_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, df_data))
    df_close = d_data['actual_close']
    means = pd.rolling_mean(df_close,20,min_periods=20)
    #print means
    stds = pd.rolling_std(df_close, 20)
    #print stds
    bol_val = df_close.add(-means, fill_value = 0).div(stds, fill_value=0)

    print bol_val

    print df_close

                
                    


           