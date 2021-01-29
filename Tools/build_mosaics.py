# -*- coding: utf-8 -*-
"""
Extracts a list of raster image paths form a CSV file and adds to a mosaic dataset.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os
import sys

import arcpy


def open_csv_read(filename):
    """Open a file for CSV reading in a Python 2 and 3 compatible way."""
    if sys.version_info[0] < 3:
        return open(filename, "rb")
    return open(filename, "r", encoding="utf8", newline="")


def load_csv_file(csvpath):
    records = []
    with open_csv_read(csvpath) as csv_file:
        csv_reader = csv.reader(csv_file)
        # ignore the first record (header)
        next(csv_reader)
        for row in csv_reader:
            if sys.version_info[0] < 3:
                row = [item.decode("utf-8") for item in row]
            records.append(row)
    return records


def make_raster_list_for_mosaic(fgdb, mosaic, csv_data):
    raster_path_index = 0
    rasters = []
    for record in csv_data:
        if record[raster_path_index] is not None:
            rasters.append(record[raster_path_index])
    return rasters


def add_rasters_to_mosaic(fgdb, mosaic, rasters):
    dataset = os.path.join(fgdb, mosaic)
    arcpy.AddRastersToMosaicDataset_management(
        in_mosaic_dataset=dataset,
        raster_type="Raster Dataset",
        input_path=rasters,
        update_overviews="NO_OVERVIEWS",
    )


def main(fgdb, mosaic, csv_file):
    csv_data = load_csv_file(csv_file)
    rasters = make_raster_list_for_mosaic(fgdb, mosaic, csv_data)
    print("Adding {0} rasters to {1}".format(len(rasters), mosaic))
    add_rasters_to_mosaic(fgdb, mosaic, rasters)


if __name__ == "__main__":
    gdb = r"C:/tmp/topo/USGS_Topo_Maps.gdb"
    main(fgdb=gdb, mosaic="Current_1to25k", csv_file=r"new_files.txt")
