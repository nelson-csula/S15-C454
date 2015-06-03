__author__ = 'Michael'
import re
import bson
from dateutil.parser import parse
import datetime
import dateutil
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Install pymongo first!!
# pip install pymongo

# Start mongod before running
from pymongo import MongoClient

mongo = MongoClient()
db = mongo.bigDataTest

# ##################################################################
# dates = pd.date_range('20130101', periods=6);
# # print dates;
#
# data = np.random.randn(6,1);
# columnList = 'A';
#
# df = pd.DataFrame( data, index=dates, columns=list(columnList) );
# # print df;
#
# ##################################################################
# dates1 = pd.date_range('20140101', periods=7);
# # print dates;
#
# data1 = np.random.randn(6,1);
# columnList = 'A';
#
# df1 = pd.DataFrame( data1, index=dates1, columns=list(columnList) );
# # print df;
#
# r = df.corr(df1);
#
# print r;

data1 = np.random.randn(6,1)[0];
data2 = np.random.randn(6,1)[0];

print np.correlate(data1,data2);


# def getData(start_date, day_count, crime, zip):
#
#     day_count = day_count + 1;
#     d = 0;
#     start_date_count = 0;
#     for single_date in (start_date + datetime.timedelta(n) for n in range(day_count)):
#         d = d + 1;
#         if single_date == start_date:
#             continue;
#
#         found = db.crimes.find({
#             "parsedDate" : {"$gte": start_date}, "parsedDate": { "$lte": single_date }, "zip": zip
#         }).count();
#
#         if d == 2:
#             start_date_count = found;
#
#         print start_date, single_date, start_date_count, found;
#
# dt_obj = datetime.datetime.strptime('2014-01-01', '%Y-%m-%d')
# print getData( dt_obj, 7, "LARCENY THEFT", "90013" );

# COLUMN_SEPARATOR = '  '
# housing_data = pd.DataFrame.from_csv('housing.csv', sep=COLUMN_SEPARATOR, header=None)

x = data1; # housing_data[AREA_INDEX]
y = data2; # housing_data[SELLING_PRICE_INDEX]
regression = np.polyfit(x, y, 1);

print regression;
