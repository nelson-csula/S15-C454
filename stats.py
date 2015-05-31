import urllib
import dateutil.parser as dateparser
import re
import urllib2
import xmltodict
import json
import BeautifulSoup as bs
from pprint import pprint
from xml.dom import minidom
from HTMLParser import HTMLParser
from pymongo import MongoClient
import csv
import statistics
import numpy
import math
import time
import calendar
import collections

from numpy import cumprod, linspace, random

from bokeh.charts import BoxPlot, output_file, show, Bar
from bokeh.plotting import figure, show, output_file, vplot, figure, output_file, show
import re
import bson
from dateutil.parser import parse
import datetime
import dateutil
from pymongo import MongoClient
from bokeh.models import HoverTool, BoxSelectTool
from itertools import groupby
import collections
import pandas as pd


###############################################################
## Data Acquisition Main()

debug = 0

# DB client
mongo = MongoClient()
db = mongo.bigDataTest

pipeline = [
   {
     "$group": {
        "_id": "$zip",
        "total": { "$sum": 1 }
     }
   }
];

sumByZip = db.crimes.aggregate( pipeline );

counts = []

for zipEntry in sumByZip:
    if len(zipEntry["_id"]) > 0 and zipEntry["_id"].isdigit():
        zipCode = int(zipEntry["_id"]);
        if zipCode > 90000:
            print zipCode, "=", zipEntry["total"];
            counts.append( zipEntry["total"] );

print counts;

# def average(s): return sum(s) * 1.0 / len(s)
# def variance(s): return map(lambda x: (x - avg)**2, s)
# def std_dev(v): return math.sqrt(average(v))
# avg = average(counts)
# v = variance(counts)
# s = std_dev(v);

medianValue = statistics.median(counts);
avg = statistics.mean(counts);
mode = statistics.mode(counts);
stdev = statistics.stdev(counts);
stdev2 = numpy.std(counts);

print "==============================";
print "mean/avg crimes per zipcode", avg;
print "median crimes per zipcode", medianValue;
print "mode crimes per zipcode", mode;
print "stdev crimes per zipcode", stdev;



def plotPoints(xvalues, countValues, filename, titleValue, legendValue, points):
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"
    output_file(filename, title=titleValue)

    plot = figure( tools=TOOLS, width=1500, height = 1000); # width=300, height=300
    plot.line(xvalues, countValues, legend=legendValue, line_color="blue")
    plot.circle(xvalues, countValues, legend = legendValue, fill_color="blue", line_color="blue", size=5);

    for k in points.keys():
        print " * ", k, "x = ", points[k]["x"];
        x = [ points[k]["x"] ];
        y = [ 0 ];
        l = points[k]["legend"];
        c = points[k]["color"];
        s = points[k]["size"];
        plot.circle(x, y, legend = l, fill_color=c, line_color=c, size=s);

    show(plot)

def frequency(countValues):
    return [len(list(group)) for key, group in groupby(countValues)];

def frequency2(countValues):
    v1 = collections.Counter(countValues);
    v2 = collections.OrderedDict(sorted(v1.items()));
    return v2;

def indexedArray(input):
    result = [];
    for idx, i in enumerate(input): # for idxUniqueDate, u in enumerate(uniqueDates)
        result.append(idx);
    return result;

# add stats to list
counts.append(avg);
counts.append(avg + stdev);
# counts.append(avg - stdev);

sortedCounts = sorted(counts);
xaxis = indexedArray(sortedCounts);

plotPoints(xaxis, sortedCounts, "totals.html", "total crimes by zipcode", "all crimes by zipcode", {} );


f = frequency2(sorted(counts));
print f.keys(); # counts
print f.values(); # frequency

statPoints = {};
statPoints["mean"] = { };
statPoints["mean"]["x"] = avg;
statPoints["mean"]["legend"] = "Avg/Mean";
statPoints["mean"]["color"] = "red";
statPoints["mean"]["size"] = 20;

statPoints["median"] = { };
statPoints["median"]["x"] = medianValue;
statPoints["median"]["legend"] = "Median";
statPoints["median"]["color"] = "green";
statPoints["median"]["size"] = 20;

statPoints["mode"] = { };
statPoints["mode"]["x"] = mode;
statPoints["mode"]["legend"] = "Mode";
statPoints["mode"]["color"] = "yellow";
statPoints["mode"]["size"] = 20;

statPoints["stdev"] = { };
statPoints["stdev"]["x"] = stdev;
statPoints["stdev"]["legend"] = "Std Dev";
statPoints["stdev"]["color"] = "purple";
statPoints["stdev"]["size"] = 20;


# print "median crimes per zipcode", medianValue;
# print "mode crimes per zipcode", mode;
# print "stdev crimes per zipcode", stdev;



plotPoints(f.keys(), f.values(), "frequency.html", "frequency of counts", "frequency of crime counts by zipcode", statPoints);


#
# # db.Listing.find().forEach(function(item){
# #     db.Listing.update({_id: item._id}, {$set: { LowerCaseAddress: item.Address.toLowerCase() }})
# # })
#
# def read_file(filename):
#     with open(filename, 'r') as f:
#         data = [row for row in csv.reader(f.read().splitlines())]
#     return data
#
#
# csv_path = "2010+Census+Population+By+Zipcode+(ZCTA).csv"
# cr = read_file(csv_path);
#
# for row in cr:
#     zipcode = row[0];
#     population = row[1];
#     print "searching for zip", zipcode, "..."
#     matchingzip = db.crimes.find( { "zip": zipcode }  ); #     sourceNews = db.news.find({"source": s["name"]}).count()
#     print " => found ", matchingzip.count(), "matches"
#     for match in matchingzip:
#         db.crimes.update(  { "_id": match["_id"] }, { "$set": { "population" : population }  } );
#
#
# # # get_neighborhood_for_crimes()
# # # exit(0)
# #
# # # Sheriff's Department Data
# # # http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv
# #
# # print "Loading Sheriff's crimes database..."
# #
# # csv_path = "2014-PART_I_AND_II_CRIMES.csv"
# # with open(csv_path, "rb") as csvfile:
# #     cr = csv.reader(csvfile)
# #
# #     for row in cr:
# #         # add_crimes(row[11], row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[15], row[16])
# #         # (          id      , incidentDate, category, stat  , statDesc, addressStreet, city  , zip   , xCoor , yCoor  , incidentId, reportDistrict, seq    , unitId , unitName, deleted):
# #         add_crimes(row[11] , row[0]      , row[2]  , row[3], row[4]  , row[5]       , row[7], row[8], row[9], row[10], row[11]   , row[12]       , row[13], row[15], row[16] , row[17]);
# #
# #         # print "incidentDate", row[0]
# #         # print "incidentReportedDate", row[1]
# #         # print "category", row[2]
# #         # print "state", row[3]
# #         # print "statDesc", row[4]
# #         # print "address", row[5]
# #         # print "street", row[6]
# #         # print "city", row[7]
# #         # print "zip", row[8]
# #         # print "xCoor", row[9]
# #         # print "yCoor", row[10]
# #         # print "incidentId", row[11]
# #         # print "reportingDistrict", row[12]
# #         # print "seq", row[13]
# #         # print "gangRelated", row[14]
# #         # print "unitId", row[15]
# #         # print "unitName", row[16]
# #         # print "deleted", row[17]
# #         #
# #         # break
#
#

#plot points by zip code from 0 to n