# -*- coding: utf-8 -*-
"""
Creates and/or clears a set of subfolders

Edit (or at least review) the Config properties before running.

Works with Python 2.7+ and Python 3.3+

These folders are not part of the code repo but are assumed by other
steps in the topo map processing scripts.  This script should be run
after cloning the repo to a new work folder, or when reprocessing
in a work folder used previously to process topo maps.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import errno
import os
import shutil
import sys


class Config(object):
    """Namespace for configuration parameters. Edit as needed."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # The working folder where input/output files can be found
    # This is the root folder of the cloned code repository.
    work_folder = "B:\\work\\USGS-Topo-Processing"

    # Should any existing subfolder be deleted?
    # Typically set to True, however False bay be helpful during testing,
    # or in atypical situations.
    delete_folders = True

    # Should the missing subfolders be created?
    # Typically set to True, however False bay be helpful during testing,
    # or to clean the repo when done.
    create_folders = True

    # The list of folders to clear/create; will be done in the work_folder
    folder_list = [
        "CurrentGeoPDF",
        "CurrentGeoTIFF",
        "Historical_QM",
        "Historical_ITM",
        "Historical_QQ",
        "Scratch",
        "Downloads",
    ]

    # The list of sub-folders to clear/create in the download folder
    # the name of the download folder is given by an index into the folder_list
    download_folder_index = 6
    download_folders = ["QQ", "QM", "ITM", "TOPO"]


def clear_existing_folders():
    """Removed existing sub folders listed in the Config object."""

    root = Config.work_folder
    for folder in Config.folder_list:
        path = os.path.join(root, folder)
        remove_tree(path)


def make__missing_folders():
    """Creates missing sub folders listed in the Config object."""

    root = Config.work_folder
    for folder in Config.folder_list:
        path = os.path.join(root, folder)
        make_dir(path)

    # Create sub folders in the downloads folder
    downloads = Config.folder_list[Config.download_folder_index]
    root = os.path.join(root, downloads)
    for folder in Config.download_folders:
        path = os.path.join(root, folder)
        make_dir(path)


def remove_tree(path):
    """Recursively remove an existing path. Silently ignores path not found.
    
    Python 2/3 compatible.
    May throw OSError, IOError, shutil.Error
    """
    if sys.version_info[0] < 3:
        try:
            shutil.rmtree(path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
    else:
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass


def make_dir(path):
    """Make a directory if it does not exist. Silently ignores existing path.
    
    Python 2/3 compatible.
    May throw OSError, IOError.
    """
    if sys.version_info[0] < 3:
        try:
            os.mkdir(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass


if __name__ == "__main__":
    if Config.delete_folders:
        clear_existing_folders()
    if Config.create_folders:
        make__missing_folders()
