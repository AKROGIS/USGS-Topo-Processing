# -*- coding: utf-8 -*-
"""
This script moves downloaded topo maps into the PDS folder structure.

Review/edit the Config properties before executing.

Works with Python 2.7 and 3.6+
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import os

import csv23


class Config(object):
    """Namespace for configuration parameters. Edit as needed."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # The working folder where input/output files can be found
    # This is the root folder of the cloned code repository.
    work_folder = "C:\\tmp\\USGS-Topo-Processing"

    # The Alaska Region PDS (X drive) folder where the USGS topo maps will be permanently archived.
    # this must match the path in make_alaska_list.py and the therefore the
    # beginning of the values in the `pds_path_column_name` (below)
    pds_root = "X:\\Extras\\AKR\\Statewide\\Charts\\USGS_Topo"

    # The name of the additional column in all metadata files that contains the
    # path to the file in the PDS. This must match the name of the column in
    # Config.addon_column_names in the make_alaska_list.py script.
    pds_path_column_name = "PDS Path"

    # A dictionary wherein the keys are the names of the download folders
    # (relative to the `work_folder`) and the values are the names of the
    # related metadata files (relative to the `work_folder`).
    download_metadata = {
        "Downloads/ITM": "Indexes/all_metadata_itm.csv",
        "Downloads/QM": "Indexes/all_metadata_qm.csv",
        "Downloads/QQ": "Indexes/all_metadata_qq.csv",
        "Downloads/TOPO": "Indexes/all_metadata_topo.csv",
    }

    # If `dry_run` is true, then no files will be moved, instead the move
    # instruction will be printed to the standard output.
    dry_run = True


def get_paths(metadata):
    """Return a dictionary with the new path for each filename in the metadata file."""

    file_paths = {}
    csv_path = os.path.join(Config.work_folder, metadata)
    with csv23.open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = csv23.fix(next(csv_reader))
        # Get pds path index; fail hard if not found
        pds_path_index = header.index(Config.pds_path_column_name)
        for row in csv_reader:
            row = csv23.fix(row)
            pds_path = row[pds_path_index]
            local_path = pds_path.replace(Config.pds_root, Config.work_folder)
            filename = os.path.basename(local_path)
            file_paths[filename] = local_path
    return file_paths


def main():
    """Move downloaded topo maps into the appropriate sub folder."""

    for download_folder in Config.download_metadata:
        filenames = os.listdir(download_folder)
        if not filenames:
            print("{0} is empty, nothing to move.".format(download_folder))
            continue
        metadata_file = Config.download_metadata[download_folder]
        paths = get_paths(metadata_file)
        download_path = os.path.join(Config.work_folder, download_folder)
        for filename in filenames:
            old_path = os.path.join(download_path, filename)
            new_path = paths[filename]
            if Config.dry_run:
                print("move {0} to {1}.".format(old_path, new_path))
            else:
                try:
                    os.rename(old_path, new_path)
                except OSError as ex:
                    msg = "    Failed to move {0} to {1}.  Reason: {2}"
                    print(msg.format(old_path, new_path, ex))


if __name__ == "__main__":
    main()
