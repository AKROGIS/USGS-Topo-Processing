# USGS Processing Tools

This folder contains scripts (python and SQL) used to collect, organize,
categorize, process, and maintain the data in this folder, and derived
products like statewide mosaics.  For appropriate use of these scripts
see the Processing Notes below.

* add_pyramids.bat
  - a DOS batch file to run GDAL commands to add pyramids to all GeoTIFFs
    in a folder tree.  This should only be run on a folder with new files.
    It does not clear any existing pyramids, and does not check for existing
    pyramids.
* arrange_topos.py
  - Moves topos in a root folder into sub-folders (creating as needed)
    based on the root name of the topo map.  This is useful for the
    current GeoPDFs as well as the historical ITM maps.
* check_qmtopos.sql
  - A collection of SQL scripts that check the sanity of the manually
    collected data in `qm_data.csv` (after that file is imported into
    a SQL database).
* compare.py
  - Compares a National Map search results file (typically in the Indexes
    folder with a folder of downloaded files.
* create_gdal_batchfile.py
  - looks for GeoPDF files without a newer GeoTIFF file and creates a
    batch file of GDAL commands to create the missing GeoTIFF files.
* list_topos.py
  - Reads the filenames in a folder of historical topos and creates a
    CSV file with the various attributes in the filename separated into
    individual columns.  Creates the basis of a data file for categorizing
    the historical topos.  This data is joined with the mosaic footprints.
* make_uget_list.py
  - extracts the download URL from the national map search results to
    create a file suitable for input to the uget program.
* merge_search_results.py
  - Adds new (partial) search results to an older complete lists of search
    results to create an up to date complete list of search results that
    will match the downloaded files.
* pdf_diffs.py
  - Compares newly downloaded pdf files with exising downloaded pdf files.
    The national map search results may indicate that a topo has been
    updated, however this may mean that only the metadata was updated
    while the pdf content is unchanged.  This will identify "updated"
    topos that actually have no change to the PDF file.
