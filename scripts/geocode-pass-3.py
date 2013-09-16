import csv
import requests
import cStringIO
import codecs
from geopy import geocoders
g = geocoders.GoogleV3()
import time

output = []

with open('../data/combined_2001_2013-pass-2.csv', 'rU') as f:
    c = csv.reader(f, delimiter=',', quotechar='"')
    c.next()

    low_tolerance = 0.68
    high_tolerance = 0.80

    print "Geocoding low confidence results..."

    bad = 0
    rowcount = 0

    for row in c:

        if (row[11] != 'google') and (float(row[11]) >= low_tolerance and float(row[11]) <= high_tolerance):
            print "Geocoding row " + str(rowcount)
            bad += 1

            lat = ''
            lng = ''
            results = g.geocode(row[3], exactly_one=False)

            if results:
                row[9] = str(results[0][1][0])
                row[10] = str(results[0][1][1])
                row[11] = 'google-pass-3'

                time.sleep(1)
                
        output.append(row)
        rowcount += 1

print bad

fields = ['date', 'year', 'district', 'address', 'race', 'sex', 'age', 'category', 'weapon', 'lat', 'lng', 'confidence']

with open('../data/combined_2001_2013-pass-3.csv', 'wb') as f:
    print "Writing output file"

    # write header row
    wr = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=';')
    wr.writerow(fields)
    wr.writerows(output)

print "Done."