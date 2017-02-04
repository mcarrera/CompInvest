import csv
import sys
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import itertools
from datetime import date, datetime, time, timedelta



if __name__ == "__main__":
    # setup
    #print  sys.path[0]
    initialcash = 50000.00
    inputfile = 'orders.csv'
    outputfile = 'values.csv'
    file_handle = open(inputfile, 'rU')
    reader = csv.reader(file_handle, delimiter = ',')
    
    dates =[]
    ls_symbols = []
    
    #get the symbols and the df_trades we are making
    for row in reader:
        d = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        d = d + dt.timedelta(hours=16)
        if not d in dates:
            dates.append(d)
        if not row[3].strip() in ls_symbols:
            ls_symbols.append(row[3].strip())
    dates.sort()
    dt_start = min(dates) 
    dt_end =  max(dates)
    
    # all dates
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end +  timedelta(days=1), dt.timedelta(hours=16))
    
    dataobj = da.DataAccess('Yahoo')
    
    ls_keys = ['close']
    df_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    
   
    d_data = dict(zip(ls_keys, df_data))
    df_close = d_data['close']
    df_close['_CASH'] = pd.Series(1.0, index = ldt_timestamps)
    
     # create trade matrix
    df_trades = pd.DataFrame(index = ldt_timestamps, columns = ls_symbols)
    df_trades.fillna(0,  inplace=True)
    # holding matrix 
    holdings = df_trades.copy()
    
    
    cash_series = pd.Series(0, index=ldt_timestamps)
    portfolio_value = pd.Series(0, index=ldt_timestamps)
    
    
    # iterate the orders
   
   
    file_handle.seek(0)
    for row in reader:
        cash  = 0
        d = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        d = d + dt.timedelta(hours=16)
        symbol = row[3].strip()
        op = row[4].strip().lower()
        n_shares = float(row[5].strip())
        price = df_close[symbol][d]
        
        amount = int(n_shares) * price
        if(op == 'buy'):
            n_shares = n_shares
            cash = -amount 
        else:
            n_shares = n_shares * -1
            cash = amount
                
        # consider 2 trades in one day
        cash_today = cash_series.get_value(d)        
        symbol_today = df_trades.loc[d][symbol]
        
        df_trades.set_value(d, symbol, n_shares+symbol_today)
        cash_series.set_value(d, cash + cash_today)
    
   
    # Use cumulative sum to convert the trade matrix into holding matrix (?)
    for s in ls_symbols:
        df_trades[s] = df_trades[s].cumsum(axis=1)
   
    
    df_trades['_CASH'] = cash_series
    df_trades['_CASH'] = df_trades['_CASH'].cumsum(axis=1)
    # print df_trades;
    # df_trades['GOOG'].to_csv('GOOG.txt', sep=',')
    # add the initial value to each day cash so that's correct
    df_trades['_CASH'] = df_trades['_CASH'].add(pd.Series(initialcash, index=ldt_timestamps), fill_value = 0)
    
    
    
    # holdings
    df_holding = df_trades.mul(df_close, axis = 0)
    
    # good stuff to calculate the totals for each day
    df_holding['_TOTAL'] = df_holding.sum(axis=1)
    
    # write to file
    writer  = csv.writer(open(outputfile, 'wb'), delimiter = ',')
    writer.writerow(['Date', 'Value'])
    k = 0
    for row_index in df_holding.index:
        row_to_enter = [row_index, df_holding.loc[row_index]['_TOTAL']]
        # skip the last line as it was artificially introduced
        k = k + 1 
        if(k < len(df_holding.index)):
            writer.writerow(row_to_enter)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    