import csv

missing = set()
all = dict()
with open(r'B:\work\USGS-Topo-Processing\Indexes\missing geopdfs.txt') as f:
    for line in f:
        missing.add(line.strip().lower())

with open(r'B:\work\USGS-Topo-Processing\Indexes\all_metadata_topo.csv') as f:
    csvreader = csv.reader(f)
    header = next(csvreader)
    for row in csvreader:
        all[row[65].lower()] = row[64]

with open(r'B:\work\USGS-Topo-Processing\Indexes\missing_urls.txt', 'w') as f:
    for name in missing:
        f.write(all[name] + '\n')

#64,65