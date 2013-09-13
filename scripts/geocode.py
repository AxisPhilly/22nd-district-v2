import csv
import requests

with open('data/shootings_2001_2013.csv', 'wb') as f:
    c = csv.reader(f, delimiter=',', quotechar='"')

    outfile = open('data/shootings_2001_2013_geo.csv', 'wb')

    for row in c:
        address = row[3]

        r = requests.get('http://localhost:8080/maps/api/geocode/json?sensor=false%20&address=' + address)

        