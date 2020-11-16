'''
Creates and/or clears a set of subfolders

Requires Python 3.3+

These folders are not part of the code repo but are assumed by other
steps in the topo map processing scripts.  This script should be run
after cloning the repo to a new work folder, or when reprocessing
in a work folder used previously to process topo maps.
'''

import os
import shutil

CONFIG = {
    # The working folder where input/output files can be found
    # This is the root folder of the cloned code repository.
    # 'work_folder': r'C:\tmp\topo',
    'work_folder': '/Users/regan/MyRepos/USGS-Topo-Processing',
    # Should any existing subfolder be deleted?
    # Typically set to True, however False bay be helpful during testing,
    # or in atypical situations.
    'delete_folders': True,
    # Should the missing subfolders be created?
    # Typically set to True, however False bay be helpful during testing,
    # or to clean the repo when done.
    'create_folders': True,
    # The list of folders to clear/create; will be done in the work_folder
    'folder_list': [
        'CurrentGeoPDF', 'CurrentGeoTIFF', 'Historical_QM', 'Historical_ITM', 'Historical_QQ',
        'Scratch', 'Downloads'
    ],
    # The list of sub-folders to clear/create in the download folder
    # the name of the download folder is given by an index into the folder_list
    'download_folder_index': 6,
    'download_folders': ['QQ', 'QM', 'ITM', 'TOPO'],
}


def clear_existing_folders():
    """Removed existing sub folders listed in the CONFIG object."""

    root = CONFIG['work_folder']
    for folder in CONFIG['folder_list']:
        path = os.path.join(root, folder)
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass


def make__missing_folders():
    """Creates missing sub folders listed in the CONFIG object."""

    root = CONFIG['work_folder']
    for folder in CONFIG['folder_list']:
        path = os.path.join(root, folder)
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

    # Create sub folders in the downloads folder
    downloads = CONFIG['folder_list'][CONFIG['download_folder_index']]
    root = os.path.join(root, downloads)
    for folder in CONFIG['download_folders']:
        path = os.path.join(root, folder)
        try:
            os.mkdir(path)
        except FileExistsError:
            pass


if __name__ == '__main__':
    if CONFIG['delete_folders']:
        clear_existing_folders()
    if CONFIG['create_folders']:
        make__missing_folders()