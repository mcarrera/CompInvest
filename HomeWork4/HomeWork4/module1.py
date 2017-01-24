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
from yahoo_finance import Share

ls_symbols = []
with open('sp5002012.txt', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        ls_symbols.append(row[0])
ls_symbols.append('SPY')

dt_start = "2008-1-1"
dt_end = "2009-12-31"


writer = csv.writer(open('prices.csv', 'wb'), delimiter = ',')
for sym in ls_symbols:
    yahoo = Share(sym)
    hist = yahoo.get_historical(dt_start, dt_end)
    for item in hist:
        writer.writerow([item['Date'], yahoo, item['Adj_Close'], item['Close']])
    