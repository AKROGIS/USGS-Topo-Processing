# -*- coding: utf-8 -*-
"""
Compares two similar folders and prints a report of differences.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os

CONFIG = {
    # old_root is where the older 'established' files exist
    "old_root": r"X:\Extras\AKR\Statewide\Charts/USGS_Topo\Current_GeoPDF",
    # new_root is where the newer 'replacement' files exist
    "new_root": r"B:\work\topo\Current_GeoPDF",
    # Show the count of files in each location, and for each category below
    "print_summary": True,
    # Print the relative file paths in the following categories?
    # adds are relative file paths in new_root, but not old_root
    "print_adds": False,
    # extras are relative file paths in old_root, but not new_root
    "print_extras": False,
    # dups are relative file paths in both new_root and old_root
    "print_dups": True,
}


def walk_tree(root):
    """ returns a set of relative paths below root """
    paths = set()
    for folder, _, files in os.walk(root):
        for filename in files:
            relative_path = os.path.join(folder, filename).replace(root, "")
            paths.add(relative_path)
    return paths


def main():
    old_root = CONFIG["old_root"]
    new_root = CONFIG["new_root"]
    old_paths = walk_tree(old_root)
    new_paths = walk_tree(new_root)
    adds = new_paths - old_paths
    extras = old_paths - new_paths
    dups = old_paths & new_paths

    if CONFIG["print_summary"]:
        print("Summary")
        print("=======")
        print("Existing Files: {0} at {1}".format(len(old_paths), old_root))
        print("Replacement Files: {0} at {1}".format(len(new_paths), new_root))
        print("New Files: {0}".format(len(adds)))
        print("Extra Files: {0}".format(len(extras)))
        print("Duplicate Files: {0}".format(len(dups)))

    if CONFIG["print_extras"]:
        print("")
        print("Extra Files")
        print("===========")
        for name in sorted(list(extras)):
            print(name)

    if CONFIG["print_adds"]:
        print("")
        print("New Files")
        print("=========")
        for name in sorted(list(adds)):
            print(name)

    if CONFIG["print_dups"]:
        print("")
        print("Duplicate Files")
        print("===============")
        for name in sorted(list(dups)):
            print(name)


if __name__ == "__main__":
    main()
