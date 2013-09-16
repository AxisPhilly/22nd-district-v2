import csv
import requests
import cStringIO
import codecs
import re

output = []

# http://stackoverflow.com/questions/5838605/python-dictwriter-writing-utf-8-encoded-csv-files
class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8", 'replace') for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8", 'replace')
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data, 'replace')
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()

print "Starting up..."

# shootings
with open('../data/shooting_2001_2013.csv', 'rU') as f:
    c = csv.reader(f, delimiter=',', quotechar='"')
    c.next()

    print "Geocoding shootings..."

    rowcount = 0 

    for row in c:

        address = row[3] + ', Philadelphia, PA'
        address = re.sub(r'\&', 'and', address)
        r = requests.get('http://localhost:8080/street2coordinates/' + address)

        lat = ''
        lng = ''
        confidence = 0
        results = r.json().itervalues().next()

        if results:
            lat = results['latitude']
            lng = results['longitude']
            confidence = results['confidence']

        item = {
            'date': row[0],
            'year': row[1],
            'district': row[2],
            'address': address,
            'race': row[4],
            'sex': row[5],
            'age': row[7],
            'category': 'shooting',
            'weapon': 'Firearm',
            'lat': str(lat), 
            'lng': str(lng),
            'confidence': str(confidence)
        }

        output.append(item)

        rowcount += 1
        print  "Row " + str(rowcount) + " done."

    print "Finished geocoding shootings..."

# murders
with open('../data/murder_2000_2013.csv', 'rU') as f:
    c = csv.reader(f, delimiter=',', quotechar='"')
    c.next()

    print "Geocoding murders..."

    rowcount = 0

    for row in c:

        if row[2] > 2001:

            if row[5] != '':
                address = row[4] + ' ' + row[5] + ' ' + row[6] + ', Philadelphia, PA'
            else:
                address = row[4] + ' ' + row[6] + ', Philadelphia, PA'

            address = re.sub(r'\&', 'and', address)
            r = requests.get('http://localhost:8080/street2coordinates/' + address)

            lat = ''
            lng = ''
            confidence = 0
            results = r.json().itervalues().next()

            if results:
                lat = results['latitude']
                lng = results['longitude']
                confidence = results['confidence']

            item = {
                'date': row[1],
                'year': row[2],
                'district': row[3],
                'address': address,
                'race': row[8],
                'sex': row[9],
                'age': row[7],
                'category': 'murder',
                'weapon': row[12].title(),
                'lat': str(lat), 
                'lng': str(lng),
                'confidence': str(confidence)
            }

        output.append(item)

        rowcount += 1
        print  "Row " + str(rowcount) + " done."

    print "Finished geocoding murders..."

fields = ['date', 'year', 'district', 'address', 'race', 'sex', 'age', 'category', 'weapon', 'lat', 'lng', 'confidence']

with open('../data/combined_2001_2013.csv', 'wb') as f:
    print "Writing output file"

    # write header row
    dict_writer = DictUnicodeWriter(f, fields)
    dict_writer.writeheader()

    # write permits
    dict_writer.writerows(output)

print "Done."