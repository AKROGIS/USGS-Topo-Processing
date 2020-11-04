from __future__ import absolute_import, division, print_function, unicode_literals
import os
import csv

# Assumes python 2.7

# Warning; this script uses hard coded relative paths,
# and must be run in the 'USGS_Topos' folder.

search_folder = 'Historic_QQ'
output_csv = 'qq_data.csv'

def make_row(folder, filename):
    short_filename = filename.replace('AK_','').replace('_geo.tif','')
    rastername = filename.replace('.tif','')
    parts =  short_filename.split('_') + [None, folder, filename, rastername]
    return parts

def main():
    root = search_folder
    with open(output_csv, 'wb') as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerow(['name','sn','date','scale','rev','folder','file','raster'])

        for filename in [f for f in os.listdir(root) if f.lower().endswith('.tif')]:
            csv_writer.writerow(make_row(None, filename))
        for folder in [f for f in os.listdir(root) if os.path.isdir(os.path.join(root,f))]:
            for filename in [f for f in os.listdir(os.path.join(root,folder)) if f.lower().endswith('.tif')]:
                csv_writer.writerow(make_row(folder, filename))


if __name__ == '__main__':
    main()
