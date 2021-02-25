# USGS Processing Tools

This folder contains Python scripts used to collect, organize, categorize,
process, and maintain the data in the sibling folders, and derived
products like statewide mosaics.  For appropriate use of these scripts
see the [Update Instructions](Update_Instructions.md).

* `add_pyramids.bat`

  A DOS batch file to run [GDAL](https://gdal.org) commands to add pyramids to
  all GeoTIFFs in a folder tree. This should only be run on a folder with new
  files. It does not clear any existing pyramids, and does not check for
  existing pyramids.

  **TO DO:** Needs cleanup.

* `organize_downloads.py`

  Put topos in correct folder structure. This will move the files in the various
  `Download` folders to the PDS folder structure in the working directory.

  **TO DO:** Needs finishing and cleanup. Rename to `organize_downloads.py`

* `add_rasters_to_mosaics.py`

  Add new aster images to the mosaic data sets.

  **TO DO:** Needs cleanup.

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

* `make_alaska_lists.py`

  Reads a downloaded snapshot of the USGS database (as CSV) and creates the
  lists of topographic maps for Alaska.

* `make_folders.py`

  Creates and/or clears the set of folders that are not part of the code repo
  but are assumed by other steps in the processing scripts.  This script should
  be run after cloning the repo to a new work folder, or when reprocessing
  in a work folder used previously to process new topo maps.

## Additional tools

Tools that may yet be of value if they are cleaned up and documented in the
process steps.  The first update (end of 2020) was an ad hoc effort that
used a number of small scripts (below) that eventually made it into a few
well documented maintainable scripts (above).

* `compare_trees.py`

  Compares the local directories to the PDS directories, and prints a
  list of files that are new, deleted, and updated.

* `compare_files.py`

  Compares contents of a newly downloaded PDF files with existing PDF files by
  using a file hash. The USGS database may indicate that a map has been
  updated, however this may mean that only the metadata was updated
  while the PDF content is unchanged.  This will identify "updated"
  topos that actually have no change to the PDF file.
