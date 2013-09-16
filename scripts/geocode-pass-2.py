import csv
import requests
import cStringIO
import codecs
from geopy import geocoders
g = geocoders.GoogleV3()
import time

output = []

with open('../data/combined_2001_2013.csv', 'rU') as f:
    c = csv.reader(f, delimiter=',', quotechar='"')
    c.next()

    tolerance = 0.68

    print "Geocoding low confidence results..."

    rowcount = 0

    for row in c:

        if float(row[11]) < tolerance:
            print "Geocoding row " + str(rowcount)

            lat = ''
            lng = ''
            results = g.geocode(row[3], exactly_one=False)

            if results:
                row[9] = str(results[0][1][0])
                row[10] = str(results[0][1][1])
                row[11] = 'google'

                time.sleep(1)
                
        output.append(row)
        rowcount += 1

fields = ['date', 'year', 'district', 'address', 'race', 'sex', 'age', 'category', 'weapon', 'lat', 'lng', 'confidence']

with open('../data/combined_2001_2013-pass-2.csv', 'wb') as f:
    print "Writing output file"

    # write header row
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(fields)
    wr.writerows(output)

print "Done."