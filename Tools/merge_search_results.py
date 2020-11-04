from __future__ import absolute_import, division, print_function, unicode_literals
import csv

# Assumes python 2.7

# Warning; this script uses hard coded relative paths,
# and must be run in a copy of the 'USGS_Topos' folder.

# Input Files, must be CSV files with identical structure
# the additional data will replace or append to the data in base
old_search_results = 'Indexes/nationalmap_search_results_pdf_20191008.csv'
additional_search_results = 'partial_results_pdf_20191211.csv'
# Output file
new_search_results = 'nationalmap_search_results_pdf_20191211.csv'


# Index (0-based) of UID field in csv search results
uid_index = 0


def file_records(filename):
    rows = {}
    with open(filename, 'rb') as fh:
        csv_reader = csv.reader(fh)
        header = csv_reader.next()
        for row in csv_reader:
            #print(row)
            rows[row[uid_index]] = row
    return rows


def merge_records(filename, data):
    rows = []
    with open(filename, 'rb') as fh:
        csv_reader = csv.reader(fh)
        header = csv_reader.next()
        rows.append(header)
        for row in csv_reader:
            uid = row[uid_index]
            if uid in data:
                # replace updated row
                rows.append(data[uid])
                del data[uid]
            else:
                rows.append(row)
        # append new rows
        for uid in data:
            rows.append(data[uid])
    return rows


def save_data(data_list, filename):
    with open(filename, 'wb') as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerows(data_list)


def main():
    new_rows = file_records(additional_search_results)
    merged_rows = merge_records(old_search_results, new_rows)
    save_data(merged_rows, new_search_results)


if __name__ == '__main__':
    main()
