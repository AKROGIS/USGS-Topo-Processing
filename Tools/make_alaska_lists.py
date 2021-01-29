# -*- coding: utf-8 -*-
"""
Reads a USGS database snapshot and creates lists of Alaska Topo Maps

Edit the CONFIG object to set execution options and change assumptions

Works with Python 2.7 and 3.6+
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import datetime
from io import open
import os
import re
import sys

CONFIG = {
    # The working folder where input/output files can be found
    "work_folder": "B:\\work\\USGS-Topo-Processing",
    #'work_folder': '/Users/regan/MyRepos/USGS-Topo-Processing',
    # The USGS database snapshot from the downloaded zip file
    "usgs_file": "Scratch/topomaps_all.csv",
    # Set to True if you want to scan the usgs_file for all values in one or more columns.
    # Useful for validating CONFIG options before making lists.
    "print_domains": False,
    # domain_names: a list of field names to inspect/print range of values
    # domain_filter: an AND list of name and values that must match to consider row
    ### Check the range of values in the `Primary State` column, so we can use it as a filter
    # 'domain_filter': None,
    # 'domain_names': ['Primary State'],
    ### Check the range of key columns for Alaskan maps
    "domain_filter": [("Primary State", "AK")],
    "domain_names": ["Series", "Version", "Scale"],
    # Set to True if you want to check that the urls in usgs_file match the map name.
    "check_urls": False,
    "check_filter": [("Primary State", "AK")],
    # Set to False if you do not want to create the various lists (useful when checking the domains)
    "make_lists": True,
    # list_folder is the sub-folder of work_folder in which to write the list files
    # set to None to put lists in work_folder
    # list_folder will be created if it does not exits
    "list_folder": "Indexes",
    # The datestamp file contains the date of the last processing; it located in the list_folder
    "datestamp": "last_processing_date.txt",
    # Names of columns in the usgs_file that will be read by this script
    "date_column_name": "Create Date",
    "map_name_column_name": "Map Name",
    "scale_column_name": "Scale",
    "url_column_name": "Download Product S3",
    # topo_filter is a list of columns and values that must match to be a US Topo file we want
    "topo_filter": [("Primary State", "AK"), ("Series", "US Topo")],
    # htmc_filter is a list of columns and values that must match to be a HTMC topo file we want
    "htmc_filter": [("Primary State", "AK"), ("Series", "HTMC")],
    # list files to create
    # *_metadata is a CSV file with all columns for all topo maps of type *
    # *_urls is a list of download URL to new topo products of type * since the last processing date
    # The list of new/updated US Topo Maps for Alaska
    "topo_metadata": "all_metadata_topo.csv",
    "topo_urls": "new_downloads_topo.txt",
    # The list of new/updated Historic Quarter-Quad maps for Alaska
    # Any HTMC topo with a scale less than max_qq_scale will be considered quarter quad (QQ) topo
    "max_qq_scale": 30000,
    "qq_metadata": "all_metadata_qq.csv",
    "qq_urls": "new_downloads_qq.txt",
    # The list of new/updated Historic Quarter-Million maps for Alaska
    # Any HTMC topo with a scale more than min_qm_scale will be considered quarter million (QM) topo
    "min_qm_scale": 200000,
    "qm_metadata": "all_metadata_qm.csv",
    "qm_urls": "new_downloads_qm.txt",
    # The list of new/updated Historic Inch-To-Mile maps for Alaska
    # Any HTMC map that is not a QQ or QM topo will be considered inch to the mile (ITM) topo
    "itm_metadata": "all_metadata_itm.csv",
    "itm_urls": "new_downloads_itm.txt",
    # historic_scales are the various scales that were used for Historical topos in Alaska
    # This list can be determined/verified by checking the domain for 'Scale' values
    # with the domain_filter of [('Primary State','AK'), ('Series', 'HTMC')]
    "historic_scales": [24000, 25000, 250000, 50000, 62500, 63360],
    # folder_regex is a regular expression to extract the base (folder) name from the map name
    # This matches all but a few special cases covered in the map_folder() function.
    "folder_regex": re.compile(r"([A-Za-z ]+) [A-D]-[0-8].*"),
    # A regular expression for breaking a geoPDF filename into parts for building the
    # simple .tif file name
    "geopdf_regex": re.compile(
        r"AK_([A-Za-z_]+)_([A-D]-[0-8])_([SN][WE]|OE_[EWNS_]*)_[0-9]{8}_TM_geo\.pdf"
    ),
    # The Alaska Region PDS (X drive) folder where the USGS topo maps will be permanently archived.
    "pds_root": "X:\\Extras\\AKR\\Statewide\\Charts\\USGS_Topo",
    # The PDS has standard names for the folders for each type of topo map
    # this is used with pds_root to determine the full path to each topo map.
    "folder": {
        "topo": "Current_GeoPDF",
        "qq": "Historic_QQ",
        "qm": "Historic_QM",
        "itm": "Historic_ITM",
    },
}


def open_csv(filename, mode="r"):
    """
    Open a file for CSV mode in a Python 2 and 3 compatible way.

    mode must be one of "r" for reading or "w" for writing.
    """
    if sys.version_info[0] < 3:
        return open(filename, mode + "b")
    return open(filename, mode, encoding="utf8", newline="")


def write_csv_row(writer, row):
    """writer is a csv.writer, and row is a list of unicode or number objects."""
    if sys.version_info[0] < 3:
        # Ignore the pylint error that unicode is undefined in Python 3
        # pylint: disable=undefined-variable
        writer.writerow(
            [
                item.encode("utf-8") if isinstance(item, unicode) else item
                for item in row
            ]
        )
    else:
        writer.writerow(row)


def py23_fix_row(row):
    """Return a list of unicode strings from Python 2 or Python 3 strings."""
    if sys.version_info[0] < 3:
        return [item.decode("utf-8") for item in row]
    return row


def skip(row, row_filter):
    """
    Return true if this row should be ignored.

    if row_filter is None or an empty dictionary, return False
    row_filter should be a dictionary<Int,String>
    if row[Int] == String then do not skip
    """
    if not row_filter:
        return False
    for index in row_filter:
        if row[index] != row_filter[index]:
            return True
    return False


def print_domains():
    """Prints all values found in selected columns.  See CONFIG for details."""

    allfile = os.path.join(CONFIG["work_folder"], CONFIG["usgs_file"])
    column_names = CONFIG["domain_names"]
    domain_filter = CONFIG["domain_filter"]
    row_filter = {}
    domains = [
        {"name": name, "index": -1, "values": set()} for name in set(column_names)
    ]
    with open_csv(allfile, "r") as in_file:
        csvreader = csv.reader(in_file)
        header = next(csvreader)
        header = py23_fix_row(header)
        for domain in domains:
            try:
                domain["index"] = header.index(domain["name"])
            except ValueError:
                pass
        if domain_filter:
            for name, value in domain_filter:
                try:
                    index = header.index(name)
                    row_filter[index] = value
                except ValueError:
                    pass
        for row in csvreader:
            row = py23_fix_row(row)
            if not skip(row, row_filter):
                for domain in domains:
                    if domain["index"] >= 0:
                        domain["values"].add(row[domain["index"]])

    for domain in domains:
        print(domain["name"])
        if domain["index"] < 0:
            print("  ERROR: Column name not found.")
        else:
            for value in sorted(list(domain["values"])):
                print("  {0}".format(value))


def check_urls():
    """
    Checks that the map name is in the url

    In HTMC Maps, space are replaced by '%20', Periods(.) are removed,
      and ampersands(&) are replaced by 'and'
    In US Topo Maps, spaces are replaced by '_'
    """
    allfile = os.path.join(CONFIG["work_folder"], CONFIG["usgs_file"])
    check_filter = CONFIG["check_filter"]
    row_filter = {}
    with open_csv(allfile, "r") as in_file:
        csvreader = csv.reader(in_file)
        header = next(csvreader)
        header = py23_fix_row(header)
        try:
            url_index = header.index(CONFIG["url_column_name"])
        except ValueError:
            print("ERROR: URL column not found. Bailing!")
            return
        try:
            map_name_index = header.index(CONFIG["map_name_column_name"])
        except ValueError:
            print("ERROR: Map name column not found. Bailing!")
            return
        if check_filter:
            for name, value in check_filter:
                try:
                    index = header.index(name)
                    row_filter[index] = value
                except ValueError:
                    pass
        for row in csvreader:
            row = py23_fix_row(row)
            if not skip(row, row_filter):
                url = row[url_index]
                map_name = row[map_name_index]
                topo_name = map_name.replace(" ", "_")
                htmc_name = (
                    map_name.replace(" ", "%20").replace("&", "and").replace(".", "")
                )
                file_name = os.path.basename(url)
                if topo_name not in file_name and htmc_name not in file_name:
                    print("MISMATCH: {0} != {1}".format(map_name, file_name))


def htmc_pdf_to_tif(url):
    """
    Converts historic PDF URLs to TIFF URLs

    The database list contains only URLs to GeoPDFs, however the maps are also available as GeoTIFFs
    The GeoTIFF URLS were (are?) available from the NationalMap Viewer, and still exist for download
    While the GeoPDFs may be nice in some cases, the GeoTIFFs require no processing to incorporate
    into our Mosaics.

    https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/PDF/AK/24000/AK_Beechey%20Point%20B-3%20SE_353562_1970_24000_geo.pdf

    * Change `/PDF/` to `/GeoTIFF/`
    * Change `/{Scale}/` to `/`
    * Change `_geo.pdf` to `_geo.tif`

    https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/GeoTIFF/AK/AK_Beechey%20Point%20B-3%20SE_353562_1970_24000_geo.tif
    """
    new_url = url.replace("/PDF/", "/GeoTIFF/").replace("_geo.pdf", "_geo.tif")
    for scale in CONFIG["historic_scales"]:
        new_url = new_url.replace("/{0}/".format(scale), "/")
    return new_url


def map_folder(map_name):
    """
    Returns the name of the parent folder that a map will live in.

    On the PDS, the itm, and topo maps are organized into folders based on the map name
    i.e. "Baird Inlet C-3" -> "Baird Inlet".
    """
    regex = CONFIG["folder_regex"]
    name = map_name.replace(".", "")
    try:
        return regex.search(name).group(1)
    except AttributeError:
        # special cases where Map Name is unusual (returns the map name as the folder name)
        if name in ["Solomon", "Casadepaga"]:
            return name
        print("WARNING: Unable to determine folder name for {0}".format(map_name))
        return None


def tiffname_from_pdfname(name):
    """ Returns the name of the GeoTIFF file given the name of the GeoPDF file. """
    regex = CONFIG["geopdf_regex"]
    match = regex.search(name)
    basename = match.group(1).replace("_", " ")
    oe_spec = match.group(3).replace("_", " ")
    return "{0} {1} {2}.tif".format(basename, match.group(2), oe_spec)


def is_new_row(row):
    """
    Returns True or False if this row is new based on date settings in CONFIG.

    If any expected CONFIG options are not set, or the dates are invalid, the
    row is assumed to be new.
    """
    if "since_date" not in CONFIG:
        return True
    if "date_column_index" not in CONFIG:
        return True
    datefield = row[CONFIG["date_column_index"]]
    try:
        month, day, year = datefield.split("/")
        date = datetime.date(int(year), int(month), int(day))
        return date >= CONFIG["since_date"]
    except ValueError:
        return True


def patch_header(header):
    """Adds additional columns to a US Topo Header."""
    return header + ["Map Folder", "Raster Name", "AWS URL", "PDS Path"]


def patch_row(row, url, kind):
    """Adds additional columns to a US Topo Row."""
    folder = None
    if kind in ["topo", "itm"]:
        if CONFIG["map_name_column_index"] is not None:
            map_name = row[CONFIG["map_name_column_index"]]
            folder = map_folder(map_name)

    pds_path = None
    raster_name = None
    if url is not None:
        root = CONFIG["pds_root"]
        kind_folder = CONFIG["folder"][kind]
        file_name = os.path.basename(url)
        if kind == "topo":
            tif_name = tiffname_from_pdfname(file_name)
            raster_name, _ = os.path.splitext(tif_name)
        else:
            file_name = file_name.replace("%20", " ")
            raster_name, _ = os.path.splitext(file_name)
        if folder is None:
            pds_path = os.path.join(root, kind_folder, file_name)
        else:
            pds_path = os.path.join(root, kind_folder, folder, file_name)

    return row + [folder, raster_name, url, pds_path]


def make_lists():
    """Makes list of Alaska topo files for processing.  See CONFIG for details."""

    topo_filter = CONFIG["topo_filter"]
    topo_filter_indexes = {}
    htmc_filter = CONFIG["htmc_filter"]
    htmc_filter_indexes = {}
    scale_index = -1
    url_index = -1
    allfile = os.path.join(CONFIG["work_folder"], CONFIG["usgs_file"])
    if CONFIG["list_folder"] is None:
        list_folder = CONFIG["work_folder"]
    else:
        list_folder = os.path.join(CONFIG["work_folder"], CONFIG["list_folder"])
    if not os.path.exists(list_folder):
        os.mkdir(list_folder)
    topo_urls = os.path.join(list_folder, CONFIG["topo_urls"])
    topo_metadata = os.path.join(list_folder, CONFIG["topo_metadata"])
    qq_urls = os.path.join(list_folder, CONFIG["qq_urls"])
    qq_metadata = os.path.join(list_folder, CONFIG["qq_metadata"])
    qm_urls = os.path.join(list_folder, CONFIG["qm_urls"])
    qm_metadata = os.path.join(list_folder, CONFIG["qm_metadata"])
    itm_urls = os.path.join(list_folder, CONFIG["itm_urls"])
    itm_metadata = os.path.join(list_folder, CONFIG["itm_metadata"])

    # get date of last processing
    datestamp_file = os.path.join(list_folder, CONFIG["datestamp"])
    try:
        with open(datestamp_file, "r", encoding="utf-8") as datestamp_h:
            line = datestamp_h.readline()
            year, month, day = line.split("-")
            date = datetime.date(int(year), int(month), int(day))
            CONFIG["since_date"] = date
    except (IOError, ValueError):
        print(
            "WARNING: Unable to get the last processing date from {0}".format(
                datestamp_file
            )
        )

    with open_csv(allfile, "r") as all_h, open(
        topo_urls, "w", encoding="utf-8"
    ) as topo_urls_h, open_csv(topo_metadata, "w") as topo_meta_h, open(
        qq_urls, "w", encoding="utf-8"
    ) as qq_urls_h, open_csv(
        qq_metadata, "w"
    ) as qq_meta_h, open(
        qm_urls, "w", encoding="utf-8"
    ) as qm_urls_h, open_csv(
        qm_metadata, "w"
    ) as qm_meta_h, open(
        itm_urls, "w", encoding="utf-8"
    ) as itm_urls_h, open_csv(
        itm_metadata, "w"
    ) as itm_meta_h:
        csv_reader = csv.reader(all_h)
        csv_writer_topo_meta = csv.writer(topo_meta_h)
        csv_writer_qq_meta = csv.writer(qq_meta_h)
        csv_writer_qm_meta = csv.writer(qm_meta_h)
        csv_writer_itm_meta = csv.writer(itm_meta_h)
        header = next(csv_reader)
        header = py23_fix_row(header)

        # Get Indexes
        if topo_filter:
            for name, value in topo_filter:
                try:
                    index = header.index(name)
                    topo_filter_indexes[index] = value
                except ValueError:
                    pass
        if htmc_filter:
            for name, value in htmc_filter:
                try:
                    index = header.index(name)
                    htmc_filter_indexes[index] = value
                except ValueError:
                    pass
        try:
            CONFIG["date_column_index"] = header.index(CONFIG["date_column_name"])
        except (KeyError, ValueError):
            print("ERROR: Date column not found. Script will not perform as expected!")
        try:
            CONFIG["map_name_column_index"] = header.index(
                CONFIG["map_name_column_name"]
            )
        except (KeyError, ValueError):
            print(
                "ERROR: Map name column not found. Script will not perform as expected!"
            )
        try:
            scale_index = header.index(CONFIG["scale_column_name"])
        except (KeyError, ValueError):
            print("ERROR: Scale column not found. Script will not perform as expected!")
        try:
            url_index = header.index(CONFIG["url_column_name"])
        except (KeyError, ValueError):
            print("ERROR: URL column not found. Script will not perform as expected!")

        new_header = patch_header(header)

        write_csv_row(csv_writer_topo_meta, new_header)
        write_csv_row(csv_writer_qq_meta, new_header)
        write_csv_row(csv_writer_qm_meta, new_header)
        write_csv_row(csv_writer_itm_meta, new_header)

        for row in csv_reader:
            row = py23_fix_row(row)
            url = None
            if not skip(row, topo_filter_indexes):
                if url_index >= 0:
                    url = row[url_index]
                row = patch_row(row, url, "topo")
                write_csv_row(csv_writer_topo_meta, row)
                if url is not None and is_new_row(row):
                    topo_urls_h.write(url + "\n")
            elif not skip(row, htmc_filter_indexes):
                try:
                    scale = int(row[scale_index])
                except (ValueError, KeyError):
                    scale = 63360
                url = None
                new_row = is_new_row(row)
                if url_index >= 0:
                    url = htmc_pdf_to_tif(row[url_index])
                if scale < CONFIG["max_qq_scale"]:
                    row = patch_row(row, url, "qq")
                    write_csv_row(csv_writer_qq_meta, row)
                    if url is not None and new_row:
                        qq_urls_h.write(url + "\n")
                elif scale > CONFIG["min_qm_scale"]:
                    row = patch_row(row, url, "qm")
                    write_csv_row(csv_writer_qm_meta, row)
                    if url is not None and new_row:
                        qm_urls_h.write(url + "\n")
                else:
                    row = patch_row(row, url, "itm")
                    write_csv_row(csv_writer_itm_meta, row)
                    if url is not None and new_row:
                        itm_urls_h.write(url + "\n")

    # write the processing datestamp
    with open(datestamp_file, "w", encoding="utf-8") as datestamp_h:
        now = datetime.date.today().isoformat()
        datestamp_h.write(now)


if __name__ == "__main__":
    if CONFIG["print_domains"]:
        print_domains()
    if CONFIG["check_urls"]:
        check_urls()
    if CONFIG["make_lists"]:
        make_lists()
