import pandas 
import numpy 
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu

from pylab import *

#
# Prepare to read the data
#
symbols = ["AAPL"]
startday = dt.datetime(2010,11,1)
endday = dt.datetime(2009,12,31)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

dataobj = da.DataAccess('Yahoo')

adjcloses = dataobj.get_data(timestamps, symbols, "close")
actualclose = dataobj.get_data(timestamps, symbols, "actual_close")



adjcloses = adjcloses.fillna(method='backfill')

means = pandas.rolling_mean(adjcloses,20,min_periods=20)

print means