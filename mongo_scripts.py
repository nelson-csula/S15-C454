__author__ = 'Michael'
import re
import bson
from dateutil.parser import parse
import datetime
import dateutil


# Install pymongo first!!
# pip install pymongo

# Start mongod before running
from pymongo import MongoClient

mongo = MongoClient()
db = mongo.bigDataTest

allNews = db.news.find()
nprNews = db.news.find({"source": "NPR"})
kpccNews = db.news.find({"source":"KPCC"})

#for doc in allNews:
#    print (doc)

def add_neighborhood_zip(name, zip):
    exists = db.neighborhoods.find({"name": name})

    if exists.count() > 0:
        db.neighborhoods.remove( { "name": name } );

    newzip = [];
    for z in zip:
        newzip.append( str(z) );

    result = db.neighborhoods.insert_one(
        {
            "name": name
            , "zips": newzip
        }
    )
    print "Added ", name, "to neighborhoods..."


def add_crime_alias(crime, aliases):
    # Check for existing alias, delete if found
    exists = db.crime_alias.find({"crime": crime})
    if exists.count() > 0:
        db.crime_alias.remove({"crime": crime})
        # print "Crime", crime, "already exists.  Updating"

    # Insert updated alias info
    data = {}
    data['crime'] = crime
    data['alias'] = aliases
    db.crime_alias.insert_one(data)
    # print "Crime", crime, "added"

def get_cities():
    text_file = open("neighborhoods.txt", "r")
    lines = text_file.readlines()
    # print lines
    # print len(lines)
    text_file.close()
    return lines

def extract_city(text, city_list):
    for city in city_list:
        REGEX = re.compile(city)
        m = re.search(city, text, re.M|re.I)
        if m:
            return city

def add_source(name, url, format, divContainer):
    exists = db.sources.find({"name": name})

    if exists.count() == 0:
        result = db.sources.insert_one(
            {
                "name": name,
                "url": url,
                "format": format,
                "divContainer": divContainer
            }
        )
        print "Added ", name, "to sources..."
    else:
        print name, "already exists in sources."

def add_neighborhood(name):
    exists = db.neighborhoods.find({"name": name})

    if exists.count() == 0:
        result = db.neighborhoods.insert_one(
            {
                "name": name
            }
        )
        print "Added ", name, "to neighborhoods..."
    else:
        print name, "already exists in neighborhoods."



def get_crimes():

    result = {};

    dbCrimes = db.crime_alias.find()

    for c in dbCrimes:
        # Get list of aliases for each crime
        aliasList = c["alias"]
        for a in aliasList:
            # Search each article for crime
            REGEX = re.compile(a)
            crimeStories = db.news.find({ "body": {"$regex" : REGEX } })
            if crimeStories.count() > 0 :
                print "Crime" , a, "has", crimeStories.count(), "matches"
                for s in crimeStories:
                    db.news.update( { "_id": s["_id"] }, { "$set": { "crime": a } } );
                    # print "*", s["_id"];
                    result[ s["_id"] ] = { "alias": a, "crime": c["crime"] };
    return result;



def get_neighborhoods():

    result = {};

    dbNeighborhoods = db.neighborhoods.find()

    for c in dbNeighborhoods:
        # Get list of aliases for each crime
        name = c["name"]
        name = name.replace('\n', '').replace('\r', '');

        if len(name) > 0:
            # Search each article for neighborhood
            REGEX = re.compile(name)
            stories = db.news.find({ "body": {"$regex" : REGEX } })
            if stories.count() > 0 :
                print "Neighborhood" , name, "has", stories.count(), "matches"
                # update article with neighborhood name
                for s in stories:
                    db.news.update( { "_id": s["_id"] }, { "$set": { "neighborhood": name } } );
                    # print "*", s["_id"];
                    result[ s["_id"] ] = name;

    return result;



#db.sources.remove({})

# Add News Sources
add_source("NPR","http://api.npr.org/query?id=1001&apiKey=MDE3NTQ2MTM2MDE0MTcwNTkyMjRlMjc5NA001&output=json", "json", "")
add_source("KPCC", "http://feeds.scpr.org/893KpccSouthernCaliforniaNews?format=xml", "rss", "prose-body")
add_source("NBC-LA", "http://www.nbclosangeles.com/news/local/?rss=y&embedThumb=y&summary=y", "rss", "articleText")



# Add Crime Aliases: used to initialize data in mongodb
add_crime_alias("CRIMINAL HOMICIDE", ["murder", "homicide", "criminal homicide", "death"])
add_crime_alias("FORCIBLE RAPE", ["rape"])
add_crime_alias("ROBBERY", ["robbery", "theft"])
add_crime_alias("AGGRAVATED ASSAULT", ["assault"])
add_crime_alias("BURGLARY", ["burglary", "theft"])
add_crime_alias("LARCENY THEFT", ["larceny", "theft"])
add_crime_alias("GRAND THEFT AUTO", ["grand theft auto", "auto theft", "car stolen", "stolen car", "car jack", "car jacking", "car-jacking"])
add_crime_alias("ARSON", ["arson", "fire"])
add_crime_alias("FORGERY", ["forgery"])
add_crime_alias("FRAUD AND NSF CHECKS", ["fraud"])
add_crime_alias("SEX OFFENSES FELONIES", ["sex offense", "sex offender"])
add_crime_alias("SEX OFFENSES MISDEMEANORS", [])
add_crime_alias("NON-AGGRAVATED ASSAULTS", ["assault"])
add_crime_alias("WEAPON LAWS", ["weapon"])
add_crime_alias("OFFENSES AGAINST FAMILY", ["abuse"])
add_crime_alias("NARCOTICS", ["drugs", "narcotics"])
add_crime_alias("LIQUOR LAWS", [])
add_crime_alias("DRUNK / ALCOHOL / DRUGS", ["drunk", "alcohol", "alcoholic", "intoxicated"])
add_crime_alias("DISORDERLY CONDUCT", ["disorderly conduct", "fight", "fighting", "brawl"])
add_crime_alias("VAGRANCY", ["vagrant", "vagrancy", "loitering"])
add_crime_alias("GAMBLING", ["gambling"])
add_crime_alias("DRUNK DRIVING VEHICLE / BOAT", ["drunk driving", "drunk driver", "DUI", "driving while intoxicated"])
add_crime_alias("VEHICLE / BOATING LAWS", ["pulled over", "pulled-over", "speeding" "hit and run"])
add_crime_alias("VANDALISM", ["graffiti", "vandalism", "destruction of property"])
add_crime_alias("WARRANTS", ["warrant"])
add_crime_alias("RECEIVING STOLEN PROPERTY", [])
add_crime_alias("FEDERAL OFFENSES W/O MONEY", [])
add_crime_alias("FEDERAL OFFENSES WITH MONEY", [])
add_crime_alias("FELONIES MISCELLANEOUS", [])
add_crime_alias("MISDEMEANORS MISCELLANEOUS", ["arrest", "crime", "gang", "thug", "brawl", "gun", "weapon"])


dbSources = db.sources.find()

print "Sources:"
for s in dbSources:
    sourceNews = db.news.find({"source": s["name"]}).count()
    print "\t", s["name"], ":", sourceNews, "articles"

print ""
crimes = db.crimes.find().count()
print "Crimes:", crimes

crime_aliases = db.crime_alias.find().count()
print "Crime aliases:", crime_aliases

print ""
#city_list = get_cities()
#for neighborhood in city_list:
#    add_neighborhood(neighborhood);
#print "number of cities loaded", len(city_list)
#print ""



#########################################################################
# Get list of crimes
crimes = get_crimes();

#########################################################################
# Get list of neighborhoods
neighborhoods = get_neighborhoods();

def getCrimeCountByCity( nameOfCrime ):
    pipeline = [ { "$match": { "category": { "$eq": nameOfCrime } } }, {"$group" : {"_id":"$city", "count":{"$sum":1}} }, { "$group": { "_id": "$_id", "avgCount": { "$avg": "$count" } } }, { "$sort": { "avgCount": -1  }  } ];
    sum = db.crimes.aggregate( pipeline );

    count = 0;
    for zipEntry in sum:
        count = count + 1;
        print " >> ", zipEntry["_id"], zipEntry["avgCount"];
        if count == 3:
            break;

    return sum;

def getCrimeCountForNeighborhood( name, crime ):
    # 1. Get list of zip codes for neighborhood
    nList = db.neighborhoods.find( { "name": name });

    if nList.count() == 0:
        print " ^^ cannot find neighborhood named", name;
        return 0;

    # 2. For each zip code, get crime count
    for neighborhood in nList:
        totalCount = 0;
        for zip in neighborhood["zips"]:
            zipCount = db.crimes.find( { "zip": zip, "category": crime } ).count();
            # print "zip found", zip, "with count", zipCount;
            totalCount = totalCount + zipCount;
        return totalCount;
    # Return result as count for neighborhood

def getCrimeCountByDate( crime ):
    #matches = db.crimes.find( { "category": crime } );
    #for match in matches:
    #    d = match["incidentDate"];
        # d2 = dateutil.parser.parse(d);
        # print d, d2;
    print "working..."
    # pipeline = [ { "$match": { "category": { "$eq": nameOfCrime } } }, {"$group" : {"_id":"$city", "count":{"$sum":1}} }, { "$group": { "_id": "$_id", "avgCount": { "$avg": "$count" } } }, { "$sort": { "avgCount": -1  }  } ];
    # pipeline = [ { "$match": { "category": { "$eq": crime       } } }, {"$group" : {"_date": { "d": { "$substr":[ "$parsedDate",0,10  ]  }  }, "count": {"$sum": 1}  }  }, { "$sort": { "_date": 1  } } ];
    # pipeline = [ { "$match": { "category": { "$eq": crime       } } }, {"$group" : {"_date": { "$substr":[ "$parsedDate",0,10  ] }, "count": {"$sum": 1}  }  }, { "$sort": { "_date": 1  } } ];
    pipeline = [
        # Lets find our records
        {"$match":{"category":{"$eq": crime}}},

        # Now lets group on the name counting how many grouped documents we have
        {"$group":{"_id": {"$substr":[ "$parsedDate",0,10  ] }, "sum":{"$sum":1}}}
    ]

    results = db.crimes.aggregate( pipeline );
    print "done."
    return results;

#########################################################################
# Crimes where neighborhood is identified
for c in crimes.keys():
    for n in neighborhoods.keys():
        if n == c:
            print "found news story of", crimes[c]["crime"], "as", crimes[c]["alias"], "in", neighborhoods[n], ". neighborhood with the heighest occurances of this crime are:";
            sumByZip = getCrimeCountByCity( crimes[c]["crime"] );

            # how many total instances of this crime are in the database?
            crimeCount = db.crimes.find( { "category": crimes[c]["crime"] }).count();
            print " * totals for this crime:", crimeCount, "for all neighborhoods";

            # how many instances of this crime for the zip codes representing the neighborhood?
            t = getCrimeCountForNeighborhood(neighborhoods[n], crimes[c]["crime"]);
            percentRepresentation = 0;
            if int(crimeCount) > 0:
                percentRepresentation = int(t) / float(crimeCount) * 100;
            print " * totals for neighborhood", neighborhoods[n], ":",  t, "(", percentRepresentation, "%)";
            print "";

#########################################################################
# Get crime count by date
countByDate = getCrimeCountByDate("ARSON");

for c in countByDate:
    print c["_id"], "=", c["sum"];