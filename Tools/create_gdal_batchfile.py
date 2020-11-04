from __future__ import absolute_import, division, print_function, unicode_literals
import os
import re
import sys

# Assumes python 2.7
# This script looks for files in the current geopdf folder that do not have a newer
# file with the same (actually similar) name in the current geotif folder.
# These filenames are used to create a list of GDAL commands in a DOS batch file
#
# Warning; this script uses hard coded relative paths,
# and must be run in the 'USGS_Topos' folder.

pdf_root_folder = 'Current_GeoPDF'
tif_root_folder = 'Current_GeoTIFF'
output_script = 'maketifs.bat'

regex = re.compile(r'AK_([A-Za-z_]+)_([A-D]-[0-8])_([SN][WE]|OE_[EWNS_]*)_[0-9]{8}_TM_geo\.pdf')
cmd = 'gdal_translate --config GDAL_PDF_DPI 600 --config GDAL_PDF_LAYERS_OFF "Barcode,Map_Collar,Images,Map_Frame.Terrain.Shaded_Relief,Map_Frame.Projection_and_Grids" -of GTIFF -co COMPRESS=deflate "{0}" "{1}"'


def tifname_from_pdfname(name):
    match = regex.search(name)
    basename = match.group(1).replace('_', ' ')
    oe_spec = match.group(3).replace('_', ' ')
    return "{0} {1} {2}.tif".format(basename, match.group(2), oe_spec)


def main():
    with open(output_script, 'w') as fh:
        if not os.path.isdir(pdf_root_folder):
            print('Could not find the folder: "{0}", Aborting'.format(pdf_root_folder))
            sys.exit(1)
        if not os.path.isdir(tif_root_folder):
            print('Could not find the folder: "{0}", Aborting'.format(pdf_root_folder))
            sys.exit(1)
        sub_folders = [f for f in os.listdir(pdf_root_folder) if os.path.isdir(os.path.join(pdf_root_folder,f))]
        # print(sub_folders)
        for folder in sub_folders:
            pdf_folder = os.path.join(pdf_root_folder, folder)
            tif_folder = os.path.join(tif_root_folder, folder)
            try:
                os.mkdir(tif_folder)
            except OSError as ex:
                if os.path.exists(tif_folder):  
                    pass
                else:
                    raise ex
            pdfs = os.listdir(pdf_folder)
            tifs = os.listdir(tif_folder)
            for pdf in pdfs:
                pdfpath = os.path.join(pdf_folder, pdf)
                tif = tifname_from_pdfname(pdf)
                tifpath = os.path.join(tif_folder, tif)
                if os.path.exists(tifpath):
                    pdftime = os.path.getmtime(pdfpath)
                    tiftime = os.path.getmtime(tifpath)
                    if tiftime > pdftime:
                        # print("{0} is newer than {1}.  Skipping.".format(tifpath, pdfpath))
                        continue
                # print("building {0} from {1}.".format(tifpath, pdfpath))
                fh.write(cmd.format(pdfpath, tifpath) + "\n")


if __name__ == '__main__':
    main()
