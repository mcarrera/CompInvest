import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import csv

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']
    
    print "Finding Events"

    # Creating an empty dataframe
    #df_events = copy.deepcopy(df_close)
    #df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index
    k = 0
    writer = csv.writer(open('orders.csv', 'wb'), delimiter = ',')
    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]

            #print(str(ldt_timestamps[i])+"Symbol:" + s_sym + " Today: " +
            #str(f_symprice_today) + " Yest: " + str(f_symprice_yest))
            # Look for event
            f_threshold = 5.0
            if f_symprice_today < f_threshold and f_symprice_yest >= f_threshold:
                writer.writerow([ldt_timestamps[i], s_sym, "BUY", "100"])
                writer.writerow([ldt_timestamps[i] + dt.timedelta(days=5), s_sym, "BUY", "100"])



       
   


if __name__ == '__main__':
    print "Start"
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    #get list of symbols from file
    list = 'sp5002012'
    ls_symbols = dataobj.get_symbols_from_list(list)
    ls_symbols.append('SPY')

    ls_keys = ['actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)
    
    print "Done."            
