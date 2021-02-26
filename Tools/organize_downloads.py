# -*- coding: utf-8 -*-
"""
This script moves downloaded topo maps into the PDS folder structure.

Review/edit the Config properties before executing.

Works with Python 2.7 and 3.6+
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re


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


def get_folder_names(files, kind):
    """Return the name of the folder a topo map should be in."""

    if kind == ".tif":
        regex = re.compile(r"AK_([A-Za-z ]+)( [A-D]-[0-8]|_).*")
    else:
        regex = re.compile(r"AK_([A-Za-z_]+)_[A-D]-[0-8]_(OE|[SN][WE])_.*")

    file_folders = {}
    for filename in files:
        try:
            folder = regex.search(filename).group(1)
        except AttributeError:
            print("WARNING: Unable to determine folder name for {0}".format(filename))
            folder = None
        if folder is not None:
            if kind == ".pdf":
                folder = folder.replace("_", " ")
            if folder not in file_folders:
                file_folders[folder] = []
            file_folders[folder].append(filename)
    return file_folders


def main():
    """Move topo maps into the appropriate sub folder."""

    folders_to_fix = [("Historic_ITM", ".itf"), ("Current_GeoPDF", ".pdf")]
    for topo_folder, topo_ext in folders_to_fix:
        if not os.path.isdir(topo_folder):
            print('Could not find the folder: "{0}", Skipping'.format(topo_folder))
        else:
            print('Organizing files in "{0}"'.format(topo_folder))
        new_files = [
            topo for topo in os.listdir(topo_folder) if topo.lower().endswith(topo_ext)
        ]
        if new_files:
            print("  Found {0} new files.".format(len(new_files)))
            folders = get_folder_names(new_files, topo_ext)
            for topo in sorted(folders):
                # print("  Processing folder {0}".format(topo))
                files = folders[topo]
                folder = os.path.join(topo_folder, topo)
                try:
                    os.mkdir(folder)
                except OSError as ex:
                    if os.path.exists(folder):
                        pass
                    else:
                        raise ex
                for name in files:
                    src = os.path.join(topo_folder, name)
                    dst = os.path.join(folder, name)
                    # print("    Moving {0} to {1}.".format(src, dst))
                    try:
                        os.rename(src, dst)
                    except OSError as ex:
                        print(
                            "    Failed to move {0} to {1}.  Reason: {2}".format(
                                src, dst, ex
                            )
                        )


if __name__ == "__main__":
    main()
