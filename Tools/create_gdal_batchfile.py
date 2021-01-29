# -*- coding: utf-8 -*-
"""
Creates a file of GDAL commands to translate USGS Topo GeoPDFs to GeoTiffs
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open
import os
import re
import sys

# Assumes python 2.7
# This script looks for files in the current geopdf folder that do not have a newer
# file with the same (actually similar) name in the current geoTIFF folder.
# These filenames are used to create a list of GDAL commands in a DOS batch file
#
# Warning; this script uses hard coded relative paths,
# and must be run in the 'USGS_Topos' folder.


class Config(object):
    """Namespace for configuration parameters."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    pdf_root_folder = "Current_GeoPDF"
    tif_root_folder = "Current_GeoTIFF"
    output_script = "make_tiffs.bat"
    regex = re.compile(
        r"AK_([A-Za-z_]+)_([A-D]-[0-8])_([SN][WE]|OE_[EWNS_]*)_[0-9]{8}_TM_geo\.pdf"
    )
    cmd = (
        "gdal_translate --config GDAL_PDF_DPI 600 --config GDAL_PDF_LAYERS_OFF "
        + '"Barcode,Map_Collar,Images,Map_Frame.Terrain.Shaded_Relief,Map_Frame.'
        + 'Projection_and_Grids" -of GTIFF -co COMPRESS=deflate "{0}" "{1}"'
    )


def tif_name_from_pdf_name(name):
    """Return the name of the GeoTiff, given the name of the GeoPDF."""

    match = Config.regex.search(name)
    basename = match.group(1).replace("_", " ")
    oe_spec = match.group(3).replace("_", " ")
    return "{0} {1} {2}.tif".format(basename, match.group(2), oe_spec)


def main():
    """Create GDAL commands."""

    with open(Config.output_script, "w", encoding="utf-8") as out_file:
        if not os.path.isdir(Config.pdf_root_folder):
            print(
                'Could not find the folder: "{0}", Aborting'.format(
                    Config.pdf_root_folder
                )
            )
            sys.exit(1)
        if not os.path.isdir(Config.tif_root_folder):
            print(
                'Could not find the folder: "{0}", Aborting'.format(
                    Config.pdf_root_folder
                )
            )
            sys.exit(1)
        sub_folders = [
            folder
            for folder in os.listdir(Config.pdf_root_folder)
            if os.path.isdir(os.path.join(Config.pdf_root_folder, folder))
        ]
        # print(sub_folders)
        for folder in sub_folders:
            pdf_folder = os.path.join(Config.pdf_root_folder, folder)
            tif_folder = os.path.join(Config.tif_root_folder, folder)
            try:
                os.mkdir(tif_folder)
            except OSError as ex:
                if os.path.exists(tif_folder):
                    pass
                else:
                    raise ex
            pdfs = os.listdir(pdf_folder)
            # tiffs = os.listdir(tif_folder)
            for pdf in pdfs:
                pdf_path = os.path.join(pdf_folder, pdf)
                tif = tif_name_from_pdf_name(pdf)
                tif_path = os.path.join(tif_folder, tif)
                if os.path.exists(tif_path):
                    pdf_time = os.path.getmtime(pdf_path)
                    tif_time = os.path.getmtime(tif_path)
                    if tif_time > pdf_time:
                        # print("{0} is newer than {1}.  Skipping.".format(tif_path, pdf_path))
                        continue
                # print("building {0} from {1}.".format(tif_path, pdf_path))
                out_file.write(Config.cmd.format(pdf_path, tif_path) + "\n")


if __name__ == "__main__":
    main()
