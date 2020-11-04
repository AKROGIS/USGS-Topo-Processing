from __future__ import absolute_import, division, print_function, unicode_literals
import csv
import os
import urllib
import urlparse

# Assumes python 2.7

# Warning; this script uses hard coded relative paths,
# and must be run in a copy of the 'USGS_Topos' folder.

# Input File, must be a CSV file
national_map_search_results = 'Indexes/nationalmap_search_results_qq_20191212.csv'
#national_map_search_results = 'Indexes/qm_nationalmap_search_results_20190906.csv'
# Name of field in csv search results to put in output file
# must be in the header of the input file
url_field_name = 'downloadURL'
# File system folder for with downloaded files
#search_folder = 'Current_GeoPDF'
search_folder = 'Historic_QQ'
#search_extension = '.pdf'
search_extension = '.tif'


def get_filenames_from_csv(filename, field):
    names = []
    with open(filename, 'rb') as fh:
        csv_reader = csv.reader(fh)
        header = csv_reader.next()
        url_index = header.index(field)
        for row in csv_reader:
            if len(row) == 0:
                continue  # skip potential blank lines at end of file
            path = urlparse.urlparse(row[url_index]).path
            name = urllib.unquote(os.path.basename(path))
            names.append(name)
    return names


def get_filenames_from_folder(folder, extension):
    names = []
    for root, folders, files in os.walk(folder):
        for filename in files:
            if filename.endswith(extension):
                names.append(filename)
    return names


def main():
    csv_names = get_filenames_from_csv(national_map_search_results, url_field_name)
    fs_names = get_filenames_from_folder(search_folder, search_extension)
    csv_set = set(csv_names)
    fs_set = set(fs_names)
    print("Found {0} unique file names among {1} file names in the download urls".format(len(csv_set), len(csv_names)))
    print("Found {0} unique file names among {1} file names in the file system".format(len(fs_set), len(fs_names)))
    missing = csv_set - fs_set
    extras = fs_set - csv_set
    if len(extras) > 0:
        print("Rats!  There are {0} extra files in the file system".format(len(extras)))
        for item in extras:
            print("  {0}".format(item))
    elif len(missing) > 0:
        print("Rats!  There are {0} files missing from the file system".format(len(missing)))
        for item in missing:
            print("  {0}".format(item))
    else:
        print("100% match!")


if __name__ == '__main__':
    main()
