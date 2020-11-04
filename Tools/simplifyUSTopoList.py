import csv
import datetime

"""
The following fields are generally populated for both US Topo and HTMC maps.
The preceeding number is the field number, which is useful for script writers.
Programmers note that this list starts counting at 1.

 -1  Series
 2  Version
 3  Cell ID
 4  Map Name
 -5  Primary State
 6  Scale
 7  Date On Map
17  Datum
18  Projection
44  Cell Name
-45  Primary State Name
46  N Lat
47  W Long
48  S Lat
49  E Long
-51  Download GeoPDF
52  View FGDC Metadata XML
-53  View Thumbnail Image
55  GDA Item ID
56  Create Date
-57  Byte Count
58  Grid Size
59  Download Product S3
-60  View Thumbnail Image S3
61  NRN
62  NSN
"""
infile = 'AlaskaHTMC.csv'
outfile = 'AlaskaHTMCSimplified.csv'
columns = [1,2,3,5,6,16,17,43,45,46,47,48,51,54,55,57,58,60,61]
# Set sincedate = None to select all rows
sincedate = datetime.date(2019,12,11)
dateindex = 55


def reduce_row(row):
    newrow = []
    for index in columns:
        newrow.append(row[index])
    return newrow

def new_row(row):
    datefield = row[dateindex]
    month,day,year = datefield.split('/')
    date = datetime.date(int(year), int(month), int(day))
    return date >= sincedate
    

with open(infile) as inhandle, open(outfile, 'wb') as outhandle:
    csvreader = csv.reader(inhandle)
    csvwriter = csv.writer(outhandle)
    header = csvreader.next()
    newheader = reduce_row(header)
    csvwriter.writerow(newheader)
    for row in csvreader:
        if sincedate is None or new_row(row):
            csvwriter.writerow(reduce_row(row))
