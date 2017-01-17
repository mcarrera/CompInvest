# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
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
    
    cash = {}
    portfolio = {}
    totals = {}
    dates =[]
    ls_symbols = []
    for row in reader:
        d = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        d = d + dt.timedelta(hours=16)
        cash[d] = 0
        portfolio[d] = 0
        dates.append(d)
        if not row[3].strip() in ls_symbols:
            ls_symbols.append(row[3].strip())
            
   
    ls_symbols.sort()
        
    dt_start =   min(dates) 
    dt_end =   max(dates)
    # add 1 day
    dt_end = dt_end +  timedelta(days=1)
   
        
    #get data
     
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    
    ls_keys = ['actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    
   
    d_data = dict(zip(ls_keys, ldf_data))
   
#    print d_data['actual_close']['AAPL']['2008-12-04 16:00:00']
    
    # execute the orders
   
    file_handle.seek(0)
    today_cash = initialcash
    today_portfolio = 0.0
   
    print "Initial Cash: " + str(today_cash)
    for row in reader:
        d = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        d = d + dt.timedelta(hours=16)
        symbol = row[3].strip()
        op = row[4].strip()
        n_shares = row[5].strip()
        price = d_data['actual_close'][symbol][d]
        amount = int(n_shares) * price
       
        if(op == 'BUY'):
            today_cash = today_cash - amount
            today_portfolio = today_portfolio + amount
        else:
            today_cash = today_cash + amount
            today_portfolio = today_portfolio - amount
        cash[d] = today_cash
        portfolio[d] = today_portfolio
        totals[d] = today_cash + today_portfolio
        print str(d) + ' ' + op + ' ' +n_shares + ' ' + symbol + ' @ ' + str(price) + ' = ' + str(amount)
        print "Cash: " + str(cash[d]) + " Portfolio: " + str(portfolio[d])
        print " "
        