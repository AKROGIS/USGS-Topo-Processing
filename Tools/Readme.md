# USGS Processing Tools

This folder contains Python scripts used to collect, organize, categorize,
process, and maintain the data in the sibling folders, and derived
products like statewide mosaics.  For appropriate use of these scripts
see the [Update Instructions](Update_Instructions.md).

* `add_pyramids.bat`

  A DOS batch file to run [GDAL](https://gdal.org) commands to add pyramids to
  all GeoTIFFs in a folder tree. This should only be run on a folder with new
  files. It does not clear any existing pyramids, and does not check for
  existing pyramids.  You must initialize the GDAL command line environment
  before running this script (see the comment in the script for details.)

* `add_rasters_to_mosaics.py`

  Add new aster images to the mosaic data sets.

  **TO DO:** Needs cleanup.

* `compare_files.py`

  Uses file hashing to compares the contents of a folder of newly downloaded PDF
  files with the folder of existing PDF files. the paths to the two folders are
  provide on the command line. The folder of new downloads should be provided
  first. The USGS database may indicate that updated, however this may mean that
  only the metadata was updated while the PDF content is unchanged.  This script
  will identify the PDFs that are actually "updated" and those that are
  "duplicates" and can be deleted.

* `compare_pds_to_metadata.py`

  Checks the PDS (X Drive) paths in the metadata files.
  The metadata files are created with `make_alaska_lists.py` and they
  contain paths to the permanent resources on the PDS.  These paths should
  be checked whenever the metadata files are created.  Errors could be
  introduced if the PDS files are edited, if the USGS database changes, or if
  the processing scripts change.

* `create_gdal_batchfile.py`

  looks for GeoPDF files without a newer GeoTIFF file and creates a
  batch file of GDAL commands to create the missing GeoTIFF files.

  **TO DO:** Needs cleanup.

* `csv23.py`

  A module for safely reading and writing CSV files that may contain non-ASCII
  characters in a way that is compatible with both Python 2 and Python 3.

* `make_alaska_lists.py`

  Reads a downloaded snapshot of the USGS database (as CSV) and creates the
  lists of topographic maps for Alaska.

* `make_folders.py`

  Creates and/or clears the set of folders that are not part of the code repo
  but are assumed by other steps in the processing scripts.  This script should
  be run after cloning the repo to a new work folder, or when reprocessing
  in a work folder used previously to process new topo maps.

* `organize_downloads.py`

  Moves the files in the `Downloads` folders into the correct folder structure
  within one of the `CurrentGeoPDF` or `Historical_*` folders. The correct path
  is determined by finding the `PDS Path` in the matching
  `Indexes/all_metadata_*.csv` file and replacing the X drive prefix with the
  working folder.
