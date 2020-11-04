import csv

allfile = "topomaps_all.csv"
replacefile = "topomaps_replaced_by.csv"
topofile = "AlaskaUSTopo.csv"
htmcfile = "AlaskaHTMC.csv"

def print_domains():
    series = set()
    states = set()
    with open(allfile) as infile:
        # Skip header
        _ = infile.readline()
        csvreader = csv.reader(infile)
        for row in csvreader:
            series.add(row[0])
            states.add(row[4])
    print('series')
    print(series)
    print('states')
    print(states)

def make_files():
    with open(allfile) as all_h, \
    open(topofile,'w') as topo_h, \
    open(htmcfile,'w') as htmc_h:
        header = all_h.readline()
        topo_h.write(header)
        htmc_h.write(header)
        csvreader = csv.reader(all_h)
        csvwriter_topo = csv.writer(topo_h)
        csvwriter_htmc = csv.writer(htmc_h)
        for row in csvreader:
            if row[4] == 'AK':
                if row[0] == 'HTMC':
                    csvwriter_htmc.writerow(row)
                elif row[0] == 'US Topo':
                    csvwriter_topo.writerow(row)
                else:
                    print("Unexpected Map series value: \row[0]")

if __name__ == '__main__':
    # print_domains()
    make_files()
