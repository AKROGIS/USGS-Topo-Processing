from __future__ import absolute_import, division, print_function, unicode_literals
import arcpy
import time
import os
import csv
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def check_arcgis_ver():
    # ArcGIS version can be critical, check with user, prompt to continue
    print('Mosaic datasets are not backwards compatible, ensure users are at version {0} or higher.'.format(arcpy.GetInstallInfo()['Version']))
    raw_input('Press Enter to continue...')
    logger.info('Running ArcGIS version %s' % (arcpy.GetInstallInfo()['Version']))


def load_csv_file(csvpath):
    records = []
    with open(csvpath, 'rb') as fh:
        # ignore the first record (header)
        fh.readline()
        for row in csv.reader(fh):
            unicode_row = [unicode(item, 'utf-8') if item else None for item in row]
            records.append(unicode_row)
    return records


def make_raster_list_for_mosaic(fgdb, mosaic, csv_data):
    gdb_index = 0
    mosaic_index = 1
    raster_path_index = 0
    rasters = []
    for record in csv_data:
        # if record[gdb_index] == fgdb and record[gdb_index] == fgdb
        if record[raster_path_index] is not None:
            rasters.append(record[raster_path_index])
    return rasters


def add_rasters_to_mosaic(fgdb, mosaic, rasters):
    dataset = os.path.join(fgdb,mosaic)
    # print(dataset)
    # print(rasters)
    arcpy.AddRastersToMosaicDataset_management(
        in_mosaic_dataset=dataset,
        raster_type='Raster Dataset',
        input_path=rasters,
        update_overviews="NO_OVERVIEWS"
     )


def main(fgdb, mosaic, csv_file):

    logger.info('########################################################')
    logger.info('Run %s %s', time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"))

    #check_arcgis_ver()

    csv_data = load_csv_file(csv_file)
    rasters = make_raster_list_for_mosaic(fgdb, mosaic, csv_data)
    # logger.debug(rasters)
    logger.info('Add %s rasters to %s at %s', len(rasters), mosaic, time.strftime("%H:%M:%S"))
    add_rasters_to_mosaic(fgdb, mosaic, rasters)
    logger.info('Ended %s %s', time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"))
    logger.info('########################################################')


def main2():
    data = [
        [r'data\SDMI_SPOT5.gdb', 'SPOT5_CIR', r'data\build_spot_cir.csv'],
        [r'data\SDMI_SPOT5.gdb', 'SPOT5_RGB', r'data\build_spot_rgb.csv'],
        [r'data\SDMI_SPOT5.gdb', 'SPOT5_PAN', r'data\build_spot_pan.csv'],
        [r'data\SDMI_SPOT5.gdb', 'DEM_Ellipsoidal', r'data\build_spot_ellipsoidal.csv'],
        [r'data\SDMI_SPOT5.gdb', 'DEM_Orthometric', r'data\build_spot_orthometric.csv'],
        [r'data\ORI_IFSAR.gdb', 'ORI', r'data\build_ifsar_ori.csv'],
        [r'data\ORI_IFSAR.gdb', 'ORI_SUP', r'data\build_ifsar_ori_sup.csv'],
        [r'data\DEM_IFSAR.gdb', 'DSM', r'data\build_ifsar_dsm.csv'],
        [r'data\DEM_IFSAR.gdb', 'DTM', r'data\build_ifsar_dtm.csv']
    ]
    for gdb, mos, csv_path in data:
        main(fgdb=gdb, mosaic=mos, csv_file=csv_path)


if __name__ == '__main__':
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(logging.FileHandler(r"build-mosaics.log"))    
    logger.setLevel(logging.DEBUG)

    # main2()
    #gdb = r'X:\Mosaics\Statewide\DEMs\SDMI_IFSAR.gdb'
    gdb = r'C:/tmp/topo/USGS_Topo_Maps.gdb'
    main(fgdb=gdb, mosaic='Current_1to25k', csv_file=r'new_files.txt')
