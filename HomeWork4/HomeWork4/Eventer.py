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
    
    # Time stamps for the event range
    ldt_timestamps = df_close.index
    writer = csv.writer(open('orders.csv', 'wb'), delimiter = ',')
    # Make a list only based on the threshold
    #writer2 = csv.writer(open('list10.csv', 'wb'), delimiter = ',')
    

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps) - 5):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            #f_symprice_5days = df_close[s_sym].ix[ldt_timestamps[i + 5]]

            #print(str(ldt_timestamps[i])+"Symbol:" + s_sym + " Today: " +
            #str(f_symprice_today) + " Yest: " + str(f_symprice_yest))
            # Look for event
            f_threshold = 10.00
            if f_symprice_today / f_symprice_yest <= 0.95:
                writer.writerow([ldt_timestamps[i].year, ldt_timestamps[i].month, ldt_timestamps[i].day, s_sym, "BUY", "100"])
                writer.writerow([ldt_timestamps[i+5].year, ldt_timestamps[i+5].month, ldt_timestamps[i+5].day, s_sym, "SELL", "100"])
                #writer2.writerow([s_sym]);



       
   

if __name__ == '__main__':
    print "Start"
    dt_start = dt.datetime(2008, 1, 2)
    dt_end = dt.datetime(2009, 12, 28) + dt.timedelta(days=5)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    #get list of symbols from file
    ls_symbols = []
    list = 'sp5002012.txt'
    #list = 'list5.csv'

    with open(list, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            ls_symbols.append(row[0])
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
    print "Run the market Sym."
    
