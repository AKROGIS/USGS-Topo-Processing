"""
This script moves new topo maps into the appropriate sub folder.

The sub folder is the base name of the topo (typically the 1:250k name)
if the sub folder does not exist it is created.
it can be run after an initial bulk download, or an incremental update.

Warning; this script uses hard coded relative paths,
and must be run in the 'USGS_Topos' folder.

Assumes python 2.7
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

CONFIG = {
    # The working folder where input/output files can be found
    # This is the root folder of the cloned code repository.
    "work_folder": "B:\\work\\USGS-Topo-Processing",
    # 'work_folder': '/Users/regan/MyRepos/USGS-Topo-Processing',
    # metadata_folder is where the metadata files exist
    # if None, the metadata files are assumed to be in the work_folder
    "metadata_folder": "Indexes",
    "download_folders": "Downloads",
    "pds_folders": None,
    # downloaded files to move
    # file is the name of the file
    # column is the name of the column with a PDS path
    # raster is the name of the column with the raster name.  It should only
    # be used with the list of current topos, and is used to check the list of
    # raster files generated from the list of GeoPDFs (in column)
    "moves": [
        {
            "download_folder": "ITM",
            "pds_folder": "Historic_ITM",
            "subfolder_name": {
                "column": "Map Folder",
                "metadata": "all_metadata_itm.csv",
            },
        },
        {"download_folder": "QM", "pds_folder": "Historic_QM", "subfolder_name": None},
        {"download_folder": "QQ", "pds_folder": "Historic_QQ", "subfolder_name": None},
        {
            "download_folder": "TOPO",
            "pds_folder": "Current_GeoPDF",
            "subfolder_name": {
                "column": "Map Folder",
                "metadata": "all_metadata_topo.csv",
            },
        },
    ],
}


"""
for all files in QQ and QM move to
for all files in ITM move to Historic
"""

folders_to_fix = [("Historic_ITM", ".itf"), ("Current_GeoPDF", ".pdf")]


def get_folder_names(files, kind):
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
    for topo_folder, topo_ext in folders_to_fix:
        if not os.path.isdir(topo_folder):
            print('Could not find the folder: "{0}", Skipping'.format(topo_folder))
        else:
            print('Organizing files in "{0}"'.format(topo_folder))
        new_files = [f for f in os.listdir(topo_folder) if f.lower().endswith(topo_ext)]
        if new_files:
            print("  Found {0} new files.".format(len(new_files)))
            folders = get_folder_names(new_files, topo_ext)
            for f in sorted(folders):
                # print("  Processing folder {0}".format(f))
                files = folders[f]
                folder = os.path.join(topo_folder, f)
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
