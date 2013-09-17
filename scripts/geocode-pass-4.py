import csv
import requests
import cStringIO
import codecs
from geopy import geocoders
import os
#g = geocoders.Bing(api_key=os.environ['API_KEY'])
g = geocoders.GoogleV3()
import time

output = []

with open('../data/combined_2001_2013-pass-3.csv', 'rU') as f:
    c = csv.reader(f, delimiter=';', quotechar='"')
    c.next()

    with open('../data/combined_2001_2013-pass-5.csv', 'wb') as out:

        # write header row
        fields = ['date', 'year', 'district', 'address', 'race', 'sex', 'age', 'category', 'weapon', 'lat', 'lng', 'confidence']
        wr = csv.writer(out, quoting=csv.QUOTE_ALL, delimiter=';')
        wr.writerow(fields)

        low_tolerance = 0.68
        high_tolerance = 0.85

        print "Geocoding low confidence results..."

        bad = 0
        rowcount = 0

        for row in c:

            if (row[11] != 'google' and row[11] != 'geocoder.us') and (float(row[11]) >= low_tolerance and float(row[11]) <= high_tolerance):
                print "Geocoding row " + str(rowcount)
                bad += 1

                try:
                    results = g.geocode(row[3], exactly_one=False)
                    lat = str(results[0][1][0])
                    lng = str(results[0][1][1])
                    tolerance = 'bing'
                except (TypeError, IndexError):
                    lat = ''
                    lng = ''
                    tolerance = row[11]

                row[9] = lat
                row[10] = lng
                row[11] = tolerance

                time.sleep(0.5)
                    
            output.append(row)
            wr.writerow(row)
            rowcount += 1