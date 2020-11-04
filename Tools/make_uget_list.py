from __future__ import absolute_import, division, print_function, unicode_literals
import csv

# Assumes python 2.7

# Warning; this script uses hard coded relative paths,
# and must be run in a copy of the 'USGS_Topos' folder.

# Input File, must be a CSV file
national_map_search_results = 'Indexes/nationalmap_search_results_pdf_20191211.csv'
# Output file
uget_url_list = 'pdf_urls_for_uget.txt'
# Name of field in csv search results to put in output file
# must be in the header of the input file
url_field_name = 'downloadURL'


def get_urls(filename, field):
    urls = []
    with open(filename, 'rb') as fh:
        csv_reader = csv.reader(fh)
        header = csv_reader.next()
        url_index = header.index(field)
        #print(url_index)
        for row in csv_reader:
            #print(row)
            urls.append(row[url_index])
    return urls


def save_data(data_list, filename):
    with open(filename, 'wb') as fh:
        fh.writelines(line + '\r\n' for line in data_list)


def main():
    urls = get_urls(national_map_search_results, url_field_name)
    save_data(urls, uget_url_list)


if __name__ == '__main__':
    main()
