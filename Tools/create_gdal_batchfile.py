# -*- coding: utf-8 -*-
"""
Creates a file of GDAL commands to translate USGS Topo GeoPDFs to GeoTiffs

It gets a list of GeoPDFs from the recent downloads after they have been
organized into a local copy of the PDS (by `organize_downloads.py`).  The name
of the GeoTIFF file to create is in the metadata file created with
`make_alaska_lists.py`.  If the GeoTIFF exists and is newer than the GeoPDF,
then it is skipped.

Review/edit the Config properties before executing.

Works with Python 2.7 and 3.6+
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
from io import open
import os

import csv23


class Config(object):
    """Namespace for configuration parameters. Edit as needed."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # The working folder where input/output files can be found
    # This is the root folder of the cloned code repository.
    work_folder = "C:\\tmp\\USGS-Topo-Processing"

    # The Alaska Region PDS (X drive) folder where the USGS topo maps will be
    # permanently archived. This must match the path in make_alaska_list.py
    # and the therefore the beginning of the values in the
    # `pds_path_column_name` (below)
    pds_root = "X:\\Extras\\AKR\\Statewide\\Charts\\USGS_Topo"

    # The name of the script file to create, relative to the current working
    # directory, not the `work_folder`.
    output_script = "make_tiffs.bat"

    # The file path in `work_folder` that has the metadata for all the GeoPDFs.
    metadata = "Indexes/all_metadata_topo.csv"

    # The name of the additional column in `metadata` that contains the
    # path to the file in the PDS. This must match the name of the column in
    # Config.addon_column_names in the make_alaska_list.py script.
    pds_path_column_name = "PDS Path"

    # The name of the additional column in `metadata` that contains the
    # name of the raster for this tile. This must match the name of the column
    # in Config.addon_column_names in the make_alaska_list.py script.
    raster_name_column_name = "Raster Name"

    # The extension to add to the raster name in the metadata to create a valid
    # TIFF file name.
    tif_extension = ".tif"

    # The folder in `work_folder` that contains the GeoPDFs
    # must match the folder name in the `PDS Name` in the `metadata`
    geopdf_folder = "Current_GeoPDF"

    # The folder in `work_folder` where the GeoTIFFs will be created.
    geotiff_folder = "Current_GeoTIFF"

    # The GDAL command to execute.  Takes two parameters pdf_path and tif_path
    cmd = (
        "gdal_translate --config GDAL_PDF_DPI 600 --config GDAL_PDF_LAYERS_OFF "
        + '"Barcode,Map_Collar,Images,Map_Frame.Terrain.Shaded_Relief,Map_Frame.'
        + 'Projection_and_Grids" -of GTIFF -co COMPRESS=deflate "{0}" "{1}"\n'
    )


def read_metadata():
    """Returns a mapping of GeoPDF names to GeoTIFF names.

    The keys in the returned dictionary are the filename in the `PDS Name`
    column of the `metadata` (without the path), and the value is the
    matching `Raster Name` (without path or extension).
    """
    mapping = {}
    csv_path = os.path.join(Config.work_folder, Config.metadata)
    with csv23.open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = csv23.fix(next(csv_reader))
        # Get pds path index; fail hard if not found
        pds_path_index = header.index(Config.pds_path_column_name)
        # Get raster name index; fail hard if not found
        raster_name_index = header.index(Config.raster_name_column_name)
        for row in csv_reader:
            row = csv23.fix(row)
            pds_path = row[pds_path_index]
            # Only for testing on a unix like system
            # pds_path = pds_path.replace("\\", "/")
            pdf_name = os.path.basename(pds_path)
            raster_name = row[raster_name_index]
            mapping[pdf_name] = raster_name
    return mapping


def get_pdf_paths():
    """Returns a list of paths to GeoPDFs."""

    paths = []
    pdf_folder = os.path.join(Config.work_folder, Config.geopdf_folder)
    for directory, _, files in os.walk(pdf_folder):
        for filename in files:
            path = os.path.join(directory, filename)
            paths.append(path)
    return paths


def make_tif_path(pdf_path, metadata_info):
    """Return the path of the GeoTiff, given the path of the GeoPDF.

    metadata info is a dictionary where the key is a GeoPDF file name
    (with extension, but not path), and the value is the raster name (without
    path or extension).
    """

    pdf_folder, pdf_name = os.path.split(pdf_path)
    tif_folder = pdf_folder.replace(Config.geopdf_folder, Config.geotiff_folder)
    try:
        tif_name = metadata_info[pdf_name]
    except KeyError:
        return None
    tif_path = os.path.join(tif_folder, tif_name + Config.tif_extension)
    return tif_path


def outdated(path1, path2):
    """Returns True if path2 does not exist, or if path1 is newer than path2."""

    if not os.path.exists(path2):
        return True
    time1 = os.path.getmtime(path1)
    time2 = os.path.getmtime(path2)
    if time2 < time1:
        return True
    return False


def create_script():
    """Create a file with GDAL commands to create GeoTIFFs from GeoPDFs.

    The list of GeoPDFs comes from the filesystem.  The GeoTIFFs are created
    with the name in the metadata file in a folder mirrors the GeoPDFs.
    """

    metadata_info = read_metadata()
    pdf_paths = get_pdf_paths()
    if not pdf_paths:
        print("No GeoPDFs found. Script not necessary.")
        return

    commands = []
    for pdf_path in pdf_paths:
        tif_path = make_tif_path(pdf_path, metadata_info)
        if tif_path is None:
            msg = "ERROR: file {0} not found in the metadata. Skipping."
            print(msg.format(pdf_path))
            continue
        if outdated(pdf_path, tif_path):
            commands.append(Config.cmd.format(pdf_path, tif_path))

    if not commands:
        print("All GeoTIFFs are newer than GeoPDFs. Script not necessary.")
        return

    with open(Config.output_script, "w", encoding="utf-8") as out_file:
        out_file.writelines(commands)


if __name__ == "__main__":
    create_script()
