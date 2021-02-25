# -*- coding: utf-8 -*-
"""
Print the results of comparing two folders or files.

Folders are compared by comparing all the files within.  Files are compared
by md5 hash results.

Folder or file names to compare are provide as command line arguments.
Results are printed to the standard out (console).
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import hashlib
from io import open
import os
import sys


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
            results[name] = root.replace(folder, "")
    return results


def compare_folders(folder1, folder2):
    """Compare the contents of folder1 to folder2."""

    folders = file_map(folder2)
    for filename1 in os.listdir(folder1):
        if filename1 not in folders:
            print("new:{0}".format(filename1))
            continue
        folder = os.path.join(folder2, folders[filename1])
        # print(f2, folder)
        filename2 = os.path.join(folder, filename1)
        # print(filename1, filename2)
        if not os.path.exists(filename2):
            print("ERROR:{0} not found in {1}".format(filename1, folder))
            continue
        if md5(os.path.join(folder1, filename1)) == md5(filename2):
            print("dup:{0}".format(filename1))
        else:
            print("update:{0}".format(filename1))


def main():
    """Get the command line arguments, validate and then compare."""

    def both_files(name1, name2):
        return os.path.isfile(name1) and os.path.isfile(name2)

    def both_folders(name1, name2):
        return os.path.isdir(name1) and os.path.isdir(name2)

    if len(sys.argv) == 3 and (
        both_files(sys.argv[1], sys.argv[2]) or both_folders(sys.argv[1], sys.argv[2])
    ):
        if os.path.isfile(sys.argv[1]):
            compare_files(sys.argv[1], sys.argv[2])
        else:
            compare_folders(sys.argv[1], sys.argv[2])
    else:
        script = os.path.basename(sys.argv[0])
        msg = "Usage: python {0} file1 file2\n  or python {0} folder1 folder2"
        usage = msg.format(script)
        print(usage)


if __name__ == "__main__":
    main()
