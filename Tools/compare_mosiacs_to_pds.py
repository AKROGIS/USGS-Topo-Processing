# -*- coding: utf-8 -*-
"""
Checks the datasource paths in a raster mosaic with the PDS (X Drive) filesystem.

Folder or file names to compare are provide as Config options, or as command
line arguments, See Config. Results are printed to the standard out (console).

Works with Python 2.7+ and Python 3.3+
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os

import arcpy

import csv23


class Config(object):
    """Namespace for configuration parameters. Edit as needed."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # The geodatabase of raster mosaics. This can be the master database on the
    # PDS, or a local copy.
    mosaic_database = "X:/Mosaics/Statewide/Charts/USGS_Topo_Maps.gdb"
    # mosaic_database = "C:/tmp/topo/USGS_Topo_Maps.gdb"

    # The Alaska Region PDS (X drive) folder where the USGS topo maps are
    # permanently archived. This must match the path used to add the rasters
    # to the mosaic.
    pds_root = "X:\\Extras\\AKR\\Statewide\\Charts\\USGS_Topo"

    # The matching of mosaic raster to PDS sub folder.  You can comment out
    # pairs that you do not need to check (you know there has been no change
    # to the mosaic or filesystem since the last check.
    # You can also add some of the derived mosaics, but those will likely have
    # a long list of missing files, as they do not (by design) contain all maps.
    mosaic_folders = {
        "Current_1to25k": "Current_GeoTIFF",
        "Historic_1to63360_All": "Historic_ITM",
        "Historic_1to250k_All": "Historic_QM",
        "Historic_1to25k_All": "Historic_QQ",
    }

    # The file extension for the rasters in the mosaic.  Needed to skip extras
    # files that might be found, e.g. world files, stats, pyramids, metadata, ...
    raster_extension = ".tif"

    # If True it will write the results to CSV files with the name based on the
    # mosaic or PDS folder. The CSV has no header, and only one column which is
    # an absolute path to a raster data file. If False, the results are written
    # to the standard output (terminal screen).
    create_csv = False


def get_pds_paths(folder):
    """Returns a set of unique file paths in the folder."""

    paths = set()
    for directory, _, files in os.walk(folder):
        for filename in files:
            # skip everything but the rasters.
            if not filename.endswith(Config.raster_extension):
                continue
            path = os.path.join(directory, filename)
            paths.add(path)
    return paths


def get_mosaic_paths(datasource):
    """Returns a set of unique datasource paths in the datasource."""

    paths = set()
    # Get a temp geodatabase table name (no option to get an in memory list)
    list_table = get_scratch_table()
    arcpy.management.ExportMosaicDatasetPaths(datasource, list_table)
    fields = ["Path"]
    with arcpy.da.SearchCursor(list_table, fields) as cursor:
        for row in cursor:
            path = row[0]
            paths.add(path)
    # Delete the temp geodatabase table
    arcpy.management.Delete(list_table)
    return paths


def get_scratch_table():
    """Return the name of an unused table name in the scratch geodatabase."""

    base_name = "temp_table"
    index = 0
    table_name = "{0}{1}".format(base_name, index)
    temp_table = os.path.join(arcpy.env.scratchGDB, table_name)
    while arcpy.Exists(temp_table):
        index += 1
        table_name = "{0}{1}".format(base_name, index)
        temp_table = os.path.join(arcpy.env.scratchGDB, table_name)
    return temp_table


def compare():
    """Compare mosaics to folders."""

    for mosaic, folder in Config.mosaic_folders.items():
        mosaic_path = os.path.join(Config.mosaic_database, mosaic)
        mosaic_paths = get_mosaic_paths(mosaic_path)
        pds_path = os.path.join(Config.pds_root, folder)
        broken_links = mosaic_paths - pds_paths
        extra_rasters = pds_paths - mosaic_paths
        msg = "Comparing Mosaic: {0} to Folder: {1}"
        print(msg.format(mosaic_path, pds_path))
        pds_paths = get_pds_paths(pds_path)
        output("broken links", mosaic, broken_links)
        output("unused rasters", folder, extra_rasters)


def output(kind, name, path_list):
    """Print (or write to CSV) a list paths of kind for name.

    kind = one of "broken links" or "unused_rasters"
    """

    if path_list:
        msg = "Found {0} {1}."
        print(msg.format(len(path_list), kind))
        if Config.create_csv:
            csv_path = "{0}_in_{1}.csv".format(kind.replace(" ", "_"), name)
            with csv23.open(csv_path, "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                for path in sorted(path_list):
                    csv23.write(csv_writer, [path])
        else:
            for path in sorted(path_list):
                print(path)
    else:
        print("Found no {0}.".format(kind))


if __name__ == "__main__":
    compare()
