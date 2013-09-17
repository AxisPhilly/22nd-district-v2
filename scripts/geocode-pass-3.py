import csv
import requests
import cStringIO
import codecs
from geopy import geocoders
g = geocoders.GeocoderDotUS()
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

            try:
                results = g.geocode(row[3], exactly_one=False)
                tolerance = 'geocoder.us'
            except TypeError:
                lat = ''
                lng = ''
                tolerance = row[11]

            if place:
                row[9] = str(lat)
                row[10] = str(lng)
                row[11] = tolerance

                time.sleep(0.5)
                
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