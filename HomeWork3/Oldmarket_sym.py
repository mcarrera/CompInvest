
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
from datetime import date, datetime, time, timedelta


if __name__ == "__main__":
    
    #    initialcash = sys.argv[1];
    #    inputfile = sys.argv[2]
    #    outputfile = sys.argv[3];
    
    # setup
    initialcash = 100000.00
    inputfile = 'order.csv'
    #    outputfile = 'values.csv'
    file_handle = open(inputfile, 'rU')
    reader = csv.reader(file_handle, delimiter = ',')
    
    dates =[]
    ls_symbols = []
    orders = []
       
    for row in reader:
        d = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        d = d + dt.timedelta(hours=16)
        if not d in dates:
            dates.append(d)
        if not row[3].strip() in ls_symbols:
            ls_symbols.append(row[3].strip())
            
    dates.sort()
    dt_start =   min(dates) 
    dt_end =   max(dates)
    # add 1 day
    dt_end = dt_end 
   
        
    #get data
     
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end +  timedelta(days=1), dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    
    ls_keys = ['actual_close']
    df_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    
   
    d_data = dict(zip(ls_keys, df_data))
    df_close = d_data['actual_close']
#    df_close =  df_close[df_close.index.isin(dates)]
   
   
    df_close['_CASH'] = pd.Series(1.0, index = dates)
   
    # create trade matrix
    trades = pd.DataFrame(index = ldt_timestamps, columns = ls_symbols)
    trades.fillna(0,  inplace=True)
    # holding matrix 
    holdings = trades.copy()
    
    cash_series = pd.Series(0, index=ldt_timestamps)
    
    
    # execute the orders
   
    file_handle.seek(0)
   
    
    today_cash = initialcash
    today_portfolio = 0.0
    for row in reader:
        d = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        d = d + dt.timedelta(hours=16)
        symbol = row[3].strip()
        op = row[4].strip()
        n_shares = float(row[5].strip())
        price = df_close[symbol][d]
        
        amount = int(n_shares) * price
        if(op == 'BUY'):
            n_shares = n_shares
            today_cash = today_cash - amount  
            today_portfolio = today_portfolio + amount
        else:
            n_shares = n_shares * -1
            today_cash = today_cash + amount   
            today_portfolio = today_portfolio - amount
        
        trades.set_value(d, symbol, n_shares)    
        cash_series.set_value(d, today_cash)
      
    
    #    print type(trades)#    trades #<class 'pandas.core.frame.DataFrame'>
    
   
    for s in ls_symbols:
        trades[s] = trades[s].cumsum(axis=1)
        
   
   
    trades['_CASH'] = cash_series
    
    print trades
    print trades.mul(df_close, axis = 0)
    
     
    
      
        
        
    
    
    
    
        
       
       
        
        
    
    
    