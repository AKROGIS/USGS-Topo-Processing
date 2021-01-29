
import hashlib
from io import open
import os
import sys


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compare_files(f1, f2):
    if md5(f1) == md5(f2):
        print("Files are the same")
    else:
        print("Files are different")


def file_map(folder):
    """Returns a dictionary of filename:path for all files below folder"""
    results = {}
    for root, dirs, names in os.walk(folder):
        for name in names:
            results[name] = root.replace(folder + "\\", "")
    return results


def Compare_folders(f1, f2):
    folders = file_map(f2)
    for filename1 in os.listdir(f1):
        if filename1 not in folders:
            print("new:{0}".format(filename1))
            continue
        folder = os.path.join(f2, folders[filename1])
        # print(f2, folder)
        filename2 = os.path.join(folder, filename1)
        # print(filename1, filename2)
        if not os.path.exists(filename2):
            print("ERROR:{0} not found in {1}".format(filename1, folder))
            continue
        if md5(os.path.join(f1, filename1)) == md5(filename2):
            print("dup:{0}".format(filename1))
        else:
            print("update:{0}".format(filename1))


if __name__ == "__main__":
    if (
        len(sys.argv) != 3
        or (os.path.isfile(sys.argv[1]) and not os.path.isfile(sys.argv[2]))
        or (os.path.isdir(sys.argv[1]) and not os.path.isdir(sys.argv[2]))
        or (not os.path.isfile(sys.argv[1]) and not os.path.isdir(sys.argv[1]))
    ):
        print("Usage: {0} file1 file2".format(sys.argv[0]))
        print("    or {0} folder1 folder2".format(sys.argv[0]))
        sys.exit(1)
    if os.path.isfile(sys.argv[1]):
        compare_files(sys.argv[1], sys.argv[2])
    else:
        Compare_folders(sys.argv[1], sys.argv[2])
