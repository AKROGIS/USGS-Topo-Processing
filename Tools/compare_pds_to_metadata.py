'''
Checks the PDS (X Drive) paths in the metadata files 

The metadata files are created with `make_alaska_lists.py` and they
contain paths to the permanent resources on the PDS.  These paths should
be checked whenever the metadata files are created.  Errors could be
introduced if the PDS files are edited, or if the USGS database, or the
processing scripts change.

This script prints to the standard output (usually the terminal window):
 - a list of "Extra Paths"; paths in metadata but no matching file in the PDS.
 - a list of "Extra Files"; files in the PDS, but no matching path in the metadata.
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os

CONFIG = {
    # The working folder where input/output files can be found
    # This is the root folder of the cloned code repository.
    # 'work_folder': r'C:\tmp\topo',
    'work_folder': '/Users/regan/MyRepos/USGS-Topo-Processing',
    # metadata_folder is where the metadata files exist
    # if None, the metadata files are assumed to be in the work_folder
    'metadata_folder': 'Indexes',
    # metadata files to check
    # file is the name of the file
    # column is the name of the column with a PDS path
    # raster is the name of the column with the raster name.  It should only
    # be used with the list of current topos, and is used to check the list of
    # raster files generated from the list of GeoPDFs (in column)

    'metadata_files': [
        {
            'file': 'all_metadata_topo.csv',
            'column': 'PDS Path',
            'raster': {
                'column': 'Raster Name',
                'extension': '.tif',
                'path_transform' : ('CurrentGeoPDF', 'CurrentGeoTIFF')
            }
        },
        {
            'file': 'all_metadata_qq.csv',
            'column': 'PDS Path',
        },
        {
            'file': 'all_metadata_qm.csv',
            'column': 'PDS Path',
        },
        {
            'file': 'all_metadata_itm.csv',
            'column': 'PDS Path',
        },
    ]
}


def check_metadata_paths():
    """Checks the path columns in the metadata files."""

    metadata_paths, pds_folders = get_paths_and_folders()
    pds_files = get_pds_files(pds_folders)
    extra_paths = metadata_paths - pds_files
    if len(extra_paths):
        print("Extra Paths (in metadata, but not PDS)")
        for path in sorted(list(extra_paths)):
            print(path)
    else:
        print("Woot, Woot!, No Extra Paths")
    extra_files = pds_files - metadata_paths
    if len(extra_files):
        print("Extra Files (in PDS but not metadata)")
        for path in sorted(list(extra_files)):
            print(path)
    else:
        print("Woot, Woot!, No Extra Files")


def get_paths_and_folders():
    """Scans the metadata files to get a set of paths and folders."""

    metadata_paths = set()
    pds_folders = set()
    root = CONFIG['work_folder'] 
    metadata_folder = os.path.join(root, CONFIG['metadata_folder'])
    for metadata in CONFIG['metadata_files']:
        file_name = metadata['name']
        file_path = os.path.join(metadata_folder, file_name)
        path_column = metadata['column']
        with open(file_path) as in_file:
            csvreader = csv.reader(in_file)
            header = next(csvreader)
            try:
                path_index = header.index(path_column)
            except ValueError:
                print("WARNING: Column '{0}' not found in {1}. Skipping.".format(path_column, file_name))
                continue
            try:
                raster = metadata['raster']
            except KeyError:
                raster = None
            if raster is not None:
                try:
                    raster['index'] = header.index(raster['column'])
                except ValueError:
                    print("WARNING: Column '{0}' not found in {1}. Skipping.".format(raster['column'], file_name))
                    raster = None
            for row in csvreader:
                path = row[path_index]
                folder = os.path.dirname(path)
                metadata_paths.add(path)
                pds_folders.add(folder)
                if raster is not None:
                    name = row[raster['index']]
                    path = raster_path(name, folder, raster)
                    folder = os.path.dirname(path)
                    metadata_paths.add(path)
                    pds_folders.add(folder)

    return metadata_paths, pds_folders


def get_pds_files(folders):
    """Returns a set of unique file paths in the set of folders."""
    
    paths = set()
    for folder in folders:
        for dir, files, _ in os.walk(folder):
            for file in files:
                path = os.path.join(dir, file)
                paths.add(path)

    return paths


def raster_path(name, pdf_folder, raster):
    """
    Returns the path to a GeoTIFF raster based on the input parameters

    name: the name of the raster (without path or extension)
    pdf_folder: the path to the matching GeoPDF (provides a similar folder path)
    raster: a CONFIG object that specifies transformation parameters.
    """
    transform = raster['path_transform']
    folder = pdf_folder.replace(transform[0], transform[1])
    extension = raster['extension']
    return os.path.join(folder, name + extension)


if __name__ == '__main__':
    check_metadata_paths()