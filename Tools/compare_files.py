# -*- coding: utf-8 -*-
"""
Print the results of comparing two folders or files.

Folders are compared by comparing all the files within.  Files are compared
by md5 hash results.

Folder or file names to compare are provide as Config options, or as command
line arguments, See Config. Results are printed to the standard out (console).

Works with Python 2.7+ and Python 3.3+
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import hashlib
from io import open
import os
import sys


class Config(object):
    """Namespace for configuration parameters. Edit as needed."""

    # pylint: disable=useless-object-inheritance,too-few-public-methods

    # If False, the script will get the two objects to compare from the command line.
    use_config = True

    # The working folder where input/output files can be found
    work_folder = "B:\\Work\\USGS-Topo-Processing"

    # The location of the downloaded GeoPDFs, 
    download_pdfs = os.path.join(work_folder, "Downloads\\TOPO")

    # The Alaska Region PDS (X drive) folder where the existing GeoPDFs
    pds_pdfs = "X:\\Extras\\AKR\\Statewide\\Charts\\USGS_Topo\\Current_GeoPDF"


def md5(filename):
    """Return the md5 hash of the contents of filename."""

    hash_md5 = hashlib.md5()
    with open(filename, "rb") as in_file:
        for chunk in iter(lambda: in_file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compare_files(file1, file2):
    """Print the results of comparing the md5 hash of file1 with file2."""

    if md5(file1) == md5(file2):
        print("Files are the same")
    else:
        print("Files are different")


def file_map(folder):
    """Returns a dictionary of filename:path for all files below folder"""

    results = {}
    for root, _, names in os.walk(folder):
        for name in names:
            sub_folder = root.replace(folder, "")
            if sub_folder.startswith(os.path.sep):
                sub_folder = sub_folder[1:]
            results[name] = sub_folder
    return results


def compare_folders(folder1, folder2):
    """Compare the contents of folder1 to folder2."""

    files = os.listdir(folder1)
    if not files:
        print("{0} is empty, Nothing to compare.".format(folder1))
        return
    folders = file_map(folder2)
    # print(folders)
    for filename1 in files:
        if filename1 not in folders:
            print("new:{0}".format(filename1))
            continue
        folder = os.path.join(folder2, folders[filename1])
        # print(folder2, folder)
        filename2 = os.path.join(folder, filename1)
        # print(filename1, filename2)
        if not os.path.exists(filename2):
            print("ERROR:{0} not found in {1}".format(filename1, folder))
            continue
        if md5(os.path.join(folder1, filename1)) == md5(filename2):
            print("dup:{0}".format(filename1))
        else:
            print("update:{0}".format(filename1))


def compare(arg1, arg2):
    """Compare the two arguments (both files or both folders)."""

    if os.path.isfile(arg1):
        compare_files(arg1, arg2)
    else:
        compare_folders(arg1, arg2)



def cmdline_compare():
    """Get the command line arguments, validate and then compare."""

    def both_files(name1, name2):
        return os.path.isfile(name1) and os.path.isfile(name2)

    def both_folders(name1, name2):
        return os.path.isdir(name1) and os.path.isdir(name2)

    if len(sys.argv) == 3 and (
        both_files(sys.argv[1], sys.argv[2]) or both_folders(sys.argv[1], sys.argv[2])
    ):
        compare(sys.argv[1], sys.argv[2])
    else:
        script = os.path.basename(sys.argv[0])
        msg = "Usage: python {0} file1 file2\n  or python {0} folder1 folder2"
        usage = msg.format(script)
        print(usage)


def config_compare():
    """Compare the two objects in the Config."""

    compare(Config.download_pdfs, Config.pds_pdfs)


if __name__ == "__main__":
    if Config.use_config:
        config_compare()
    else:
        cmdline_compare()
