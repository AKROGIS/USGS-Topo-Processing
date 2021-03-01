# USGS Processing Tools

This folder contains Python scripts used to collect, organize, categorize,
process, and maintain the data in the sibling folders, and derived
products like statewide mosaics.  For appropriate use of these scripts
see the [Update Instructions](../Update_Instructions.md).

* `add_pyramids.bat`

  A DOS batch file to run [GDAL](https://gdal.org) commands to add pyramids to
  all GeoTIFFs in a folder tree. This should only be run on a folder with new
  files. It does not clear any existing pyramids, and does not check for
  existing pyramids.  You must initialize the GDAL command line environment
  before running this script (see the comment in the script for details.)

* `add_rasters_to_mosaics.py`

  Adds a list of data source (raster) paths to a raster mosaic data set.
  It does not need to be run if you know
  that there are no new rasters (i.e. no new historical topos, and all current
  files are updates to tiles already in the mosaic), but it doesn't hurt to run.
  If new rasters are added, then the mosaic footprint shape and attributes
  will need to be updated (see instructions in
  [Update Instructions](../Update_Instructions.md)).

* `compare_files.py`

  Uses file hashing to compares the contents of a folder of newly downloaded PDF
  files with the folder of existing PDF files. the paths to the two folders are
  provide on the command line. The folder of new downloads should be provided
  first. The USGS database may indicate that updated, however this may mean that
  only the metadata was updated while the PDF content is unchanged.  This script
  will identify the PDFs that are actually "updated" and those that are
  "duplicates" and can be deleted.

* `compare_mosaics_to_pds.py`
  Compares the data source paths in a raster mosaic to a specific folder (and
  sub-folders).  Can look at a set of mosaics in a file geodatabase. Results
  can be saved in a CSV (for use with `add_rasters_to_mosaics.py`), or printed
  to the terminal.  If used as input to `add_rasters_to_mosaics.py` it must be
  run on the PDS folders (after the PDS has been updated).

* `compare_pds_to_metadata.py`

  Checks the PDS (X Drive) paths in the metadata files.
  The metadata files are created with `make_alaska_lists.py` and they
  contain paths to the permanent resources on the PDS.  These paths should
  be checked whenever the metadata files are created.  Errors could be
  introduced if the PDS files are edited, if the USGS database changes, or if
  the processing scripts change.

* `create_gdal_batchfile.py`

  Looks in the `Current_GeoPDF` folder for any files without a newer matching
  file in `Current_GeoTIFF` file and creates any missing destination sub folders
  as well as a batch file of GDAL commands to create the missing GeoTIFF files.
  The correct GeoTIFF name and path is determined by finding the `PDS Path` in
  the `Indexes/all_metadata_topo.csv` file and replacing the X drive prefix with
  the working folder.

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
  within one of the `Current_GeoPDF` or `Historical_*` folders. The correct path
  is determined by finding the `PDS Path` in the matching
  `Indexes/all_metadata_*.csv` file and replacing the X drive prefix with the
  working folder.
