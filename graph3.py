# http://bokeh.pydata.org/en/latest/docs/gallery.html



# use: pip install bokeh
###########################





import time
import calendar

from numpy import cumprod, linspace, random

from bokeh.charts import BoxPlot, output_file, show, Bar
from bokeh.plotting import figure, show, output_file, vplot, figure, output_file, show
import re
import bson
from dateutil.parser import parse
import datetime
import dateutil
from pymongo import MongoClient

mongo = MongoClient()
db = mongo.bigDataTest

def f7(seq):
    seen = set();
    seen_add = seen.add;
    return [ x for x in seq if not (x in seen or seen_add(x))];

def getCrimeCountByDate( crime ):

    computed = [ "$parsedDate",0,10  ];

    pipeline = [
        # Lets find our records
        {"$match":{"category":{"$eq": crime} }, },

        # Now lets group on the name counting how many grouped documents we have
        {
            "$group": {
                "_id": {
                    "$substr": [ "$parsedDate",0,10  ]
                }
                , "sum":{"$sum":1}
            }
         },

        {
            "$sort": { "_id": 1  }
        }
    ]

    results = db.crimes.aggregate( pipeline );
    return results;

def getAsArrays(objects, key, value):
    dateList = [];
    valueList = [];

    for object in objects:
        k = object[key];
        v = object[value];
        print k , v;
        date_time = k;
        pattern = '%Y-%m-%d';
        epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000;
        dateList.append(epoch);
        valueList.append(v);

    result = { };
    result[key] = dateList;
    result[value] = valueList;
    return result;

def plotStuff():
    num_points = 300

    now = time.time()

    dt = 24*3600 # days in seconds
    dates = linspace(now, now + num_points*dt, num_points) * 1000 # times in ms

    acme = cumprod(random.lognormal(0.0, 0.04, size=num_points))
    # acme = counts;
    choam = cumprod(random.lognormal(0.0, 0.04, size=num_points))

    for p in acme:
        print p;

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    output_file("correlation.html", title="correlation.py example")

    r = figure(x_axis_type = "datetime", tools=TOOLS)

    r.line(dates, acme, color='#1F78B4', legend='ACME')
    r.line(dates, choam, color='#FB9A99', legend='CHOAM')

    r.title = "Stock Returns"
    r.grid.grid_line_alpha=0.3

    c = figure(tools=TOOLS)

    c.circle(acme, choam, color='#A6CEE3', legend='close')

    c.title = "ACME / CHOAM Correlations"
    c.grid.grid_line_alpha=0.3

    show(vplot(r, c))  # open a browser

def plotPoints(dateValues, countValues):
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    output_file("points.html", title="correlation.py example")

    plot = figure(x_axis_type = "datetime", tools=TOOLS); # width=300, height=300
    plot.line(dateValues, countValues);


    show(plot)

def plotBar(dateValues, countValues):
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    # output_file("bar.html", title="correlation.py example")

    # plot = figure(x_axis_type = "datetime", tools=TOOLS); # width=300, height=300
    # data = { "x": dateValues, "y": countValues };
    plot = Bar(dateValues, countValues, filename = "bar.html");
    plot.title("something");

    plot.show();
    # show(plot)

def timeseries():
    from collections import OrderedDict
    import datetime
    from bokeh.charts import TimeSeries, output_file, show

    # (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=1)
    dts = [now + delta*i for i in range(5)]

    xyvalues = OrderedDict({'Date': dts})
    y_python = xyvalues['python'] = [2, 3, 7, 5, 26]
    y_pypy = xyvalues['pypy'] = [12, 33, 47, 15, 126]
    y_jython = xyvalues['jython'] = [22, 43, 10, 25, 26]

    ts = TimeSeries(xyvalues, index='Date', title="TimeSeries", legend="top_left",
            ylabel='Languages')

    output_file('timeseries.html')
    show(ts)

def timeseries2(dateValues, countValues):
    from collections import OrderedDict
    import datetime
    from bokeh.charts import TimeSeries, output_file, show

    # (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=1)
    dts = [now + delta*i for i in range(5)]

    xyvalues = OrderedDict({'Date': dateValues});
    y_python = xyvalues['python'] = countValues; # [2, 3, 7, 5, 26]
    # y_python = xyvalues['python'] = [2, 3, 7, 5, 26]
    # y_pypy = xyvalues['pypy'] = [12, 33, 47, 15, 126]
    # y_jython = xyvalues['jython'] = [22, 43, 10, 25, 26]

    ts = TimeSeries(xyvalues, index='Date', title="TimeSeries", legend="top_left",
            ylabel='Languages')

    output_file('timeseries.html')
    show(ts)

def timeseries3( cats, dataMap):
    from collections import OrderedDict
    import datetime
    from bokeh.charts import TimeSeries, output_file, show

    # (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=1)
    dts = [now + delta*i for i in range(5)]

    xyvalues = OrderedDict({'Date': dataMap["date"]});
    for cat in cats:
        xyvalues[cat] = dataMap[cat]; # [2, 3, 7, 5, 26]

    # y_python = xyvalues['python'] = countValues; # [2, 3, 7, 5, 26]
    # y_python = xyvalues['python'] = [2, 3, 7, 5, 26]
    # y_pypy = xyvalues['pypy'] = [12, 33, 47, 15, 126]
    # y_jython = xyvalues['jython'] = [22, 43, 10, 25, 26]

    ts = TimeSeries(xyvalues, index='Date', title="TimeSeries", legend="top_left",
            ylabel='Crimes', width = 1500, height = 1000);

    output_file('timeseries.html')
    show(ts)


def combine(listForData, key, value):
    tmp = {};
    result = {};

    allDates = [];
    for crime in listForData:
        tmp[crime] = {};
        result[crime] = [];
        countByDate = getCrimeCountByDate(crime);
        arrayObject = getAsArrays(countByDate, key, value);
        tmp[crime][key] = arrayObject[key]; # date array
        tmp[crime][value] = arrayObject[value]; # value array

        # combine dates into one giant list
        tmpDates = allDates + tmp[crime][key];
        allDates = tmpDates;

    # dedup and sort
    uniqueDates = sorted(f7(allDates));
    print "=================";


    result["date"] = uniqueDates;
    for idxUniqueDate, u in enumerate(uniqueDates):
        # print u;
        for crime in listForData:
            v = 0;
            if u in tmp[crime][key]:
                dateIndex = tmp[crime][key].index(u);
                v = tmp[crime][value][dateIndex];
            # print u , crime , v
            result[crime].append(v);

    return result;



#########################################################################
# Get crime count by date

# countByDate = getCrimeCountByDate("ARSON");
# # countByDate2 = getCrimeCountByDate("CRIMINAL HOMICIDE");
#
# arrayObject = getAsArrays(countByDate, "_id", "sum");
# dateArray = arrayObject["_id"];
# countArray = arrayObject["sum"];
#
#
#
# # for c in countByDate:
# #     date_time = c["_id"];
# #     pattern = '%Y-%m-%d';
# #     epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000;
# #     # print epoch
# #     print epoch, "=", c["sum"];
#
# # plotPoints(dateArray, countArray);
# # plotBar(dateArray, countArray);
#
# # plotStuff();
#
# # timeseries();
#



cats = [ "ARSON", "CRIMINAL HOMICIDE", "AGGRAVATED ASSAULT", "BURGLARY", "DISORDERLY CONDUCT", "DRUNK / ALCOHOL / DRUGS", "DRUNK DRIVING VEHICLE / BOAT", "FELONIES", "FORCIBLE RAPE", "NARCOTICS"];
result = combine( cats, "_id", "sum");

timeseries3( cats, result );