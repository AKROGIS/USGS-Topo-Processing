import os
import csv


def walk_tree(root):
    """ returns a set of relative paths below root """
    paths = set()
    for folder, _, files in os.walk(root):
        for filename in files:
            # relative_path = os.path.join(folder, filename).replace(root, '')
            paths.add(filename.replace('.tif',''))
    return paths

def name_list(name):
    paths = set()
    with open(name) as fh:
        cr = csv.reader(fh)
        cr.next()
        for row in cr:
            paths.add(row[0])
    return paths

l1 = walk_tree(r'B:\work\topo\Current_GeoTIFF')
l2 = name_list(r"C:\tmp\Topo\mosaic_list.csv")

new = l1 - l2
dups = l1 & l2

#print("dups")
#for n in sorted(list(dups)):
#    print(n)
root = r"X:\Extras\AKR\Statewide\Charts\USGS_Topo\Current_GeoTIFF"
print("new")
for n in sorted(list(new)):
    base,rest = n.split('-')
    base = base[:-2]
    n2 = os.path.join(root, base, n)
    print(n2+".tif")
