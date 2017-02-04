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
import itertools
from datetime import date, datetime, time, timedelta

inputfile = 'values.csv'

# file to dataframe
df_portfolio = pd.read_csv(inputfile)
# print df_portfolio

#normalize portfolio values
#returnize
na_prices = df_portfolio['Value']
tsu.returnize0(na_prices)
#print na_prices

#volatility  (stdev of daily returns)
volatility = np.std(na_prices)

#returns
cumulative_return = np.prod(na_prices + 1) 
avg_daily_return = np.average(na_prices)
  
# sharpe ratio
#( average_daily_return/standard_deviation_of_daily_returns ) * sqrt(252)
sharpe_ratio =  (avg_daily_return  / volatility) * np.sqrt(252)

print "Standard Deviation of Fund (volatility): " + str(volatility)
print("Average Daily Return: " + str(avg_daily_return))
print("Cumulative Return: " + str(cumulative_return))
print("Sharpe Ratio: " + str(sharpe_ratio))


