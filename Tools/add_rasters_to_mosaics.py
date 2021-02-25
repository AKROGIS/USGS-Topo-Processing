# -*- coding: utf-8 -*-
"""
Extracts a list of raster image paths form a CSV file and adds to a mosaic dataset.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os

import arcpy

import csv23


def load_csv_file(csvpath):
    """Return a list of the rows in the CSV."""

    records = []
    with csv23.open(csvpath, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        # ignore the first record (header)
        next(csv_reader)
        for row in csv_reader:
            row = csv23.fix(row)
            records.append(row)
    return records


def make_raster_list_for_mosaic(csv_data):
    """Extract the names of the rasters for the CSV data."""

    raster_path_index = 0
    rasters = []
    for record in csv_data:
        if record[raster_path_index] is not None:
            rasters.append(record[raster_path_index])
    return rasters


def add_rasters_to_mosaic(fgdb, mosaic, rasters):
    """Add the list of rasters to the mosaic dataset in the fgdb."""
    dataset = os.path.join(fgdb, mosaic)
    arcpy.AddRastersToMosaicDataset_management(
        in_mosaic_dataset=dataset,
        raster_type="Raster Dataset",
        input_path=rasters,
        update_overviews="NO_OVERVIEWS",
    )


def main(fgdb, mosaic, csv_file):
    """Add the rasters in csv_file to the mosaic dataset in the fgdb."""
    csv_data = load_csv_file(csv_file)
    rasters = make_raster_list_for_mosaic(csv_data)
    print("Adding {0} rasters to {1}".format(len(rasters), mosaic))
    add_rasters_to_mosaic(fgdb, mosaic, rasters)


if __name__ == "__main__":
    main(
        fgdb=r"C:/tmp/topo/USGS_Topo_Maps.gdb",
        mosaic="Current_1to25k",
        csv_file=r"new_files.txt",
    )
