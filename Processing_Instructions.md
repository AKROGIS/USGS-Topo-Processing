# USGS Topo Map Processing Instructions

These instructions are for updating the USGS Topo map library
and mosaics maintained in the Alaska GIS PDS.  These instructions
look for changes by the USGS since the last time this process was
run and update the published products accordingly.

## Discover

In this step we get a list of download URLs for new and updated topo maps.
This is done by downloading a snapshot of the USGS database and filtering
the list to find new entries since the previous time this process was
executed.  Try to complete the Discover and Download steps in one day,
so that there is less chance of changes occurring between steps, and so
that there is a date certain as a basis for the next Discover/Download.

The USGS database has information about each map that is used in the Alaska
mosaics (like whether a historical topo map has a woodland tint).  It is
unclear when this metadata might be updated for a map.  This process assumes
that all existing maps have this metadata loaded into the Alaska mosaics,
and it does not need to be updated unless the map is new or updated.  However
it is possible that USGS might update a map's metadata without updating the
map.  Therefore it might be beneficial to update all records with the latest
database download, even if the map itself did not change.

1) Create a working directory (e.g. `C:\tmp\topo`). Referred to as `WD` below.
   - Clone or refresh repo to working directory
   - Run script to create working folders
2) Download the USGS database snapshot.
   - URL: http://thor-f5.er.usgs.gov/ngtoc/metadata/misc/topomaps_all.zip
   - Referencing web page (as of Nov. 2020):
     https://www.usgs.gov/core-science-systems/ngp/tnm-delivery/topographic-maps
3) Unzip the download to the `WD\Scratch` folder
   - There should be 3 files in this folder (1 readme, and 2 CSV files)
4) Check the check the `Change History:` at the end of `WD\Scratch\readme.txt`
   in the unzip folder for changes that might effect the scripts.
   For example adding or deleting columns in the data file.  If there have
   been changes, then any of the scripts below may fail.  If so, then the scripts
   will need to be updated to reflect the changes. In most cases, there is a
   `CONFIG` object at the beginning of the script that contains assumptions about
   the database.  Most changes can be made per the comments in the `CONFIG` object.
5) Make the download lists
   - Check and update the `CONFIG` object at the beginning of
     `WD\Tools\make_alaska_lists.py`
   - Check the file containing the date of the last processing.
     - see `CONFIG`, but typically `Indexes\last_processing_date.txt`
     - If this file does not exist, then it is assumed NO topo file have been
       previously downloaded.
   - Run `WD\Tools\make_alaska_lists.py` to create the download lists and
     metadata records for the mosaics.
6) Update the repo.
   The previous step will update various files in the `WD\Indexes` folder
   This history is retained in the repository.  Use git (or GitHub app) to
   commit and push the changes. You can use the git commit log to see the
   dates and file lists of prior updates.

## Download

The previous step generated several lists of download URLs for new/updated
topo maps.  These lists can be used to download individual files in a web
browse, or automated with uGET, curl, or a custom script.  These instructions
assume you are using [uGET](https://sourceforge.net/projects/urlget/) which is an application that does not require admin permissions.  See the
[USGS uGET page](https://viewer.nationalmap.gov/uget-instructions/) for additional instructions on installing and using uGET (ignore the instructions
for "Preparing Input Text File" as that was done in the previous step).

Each of the download lists (if not empty) should be downloaded to a
separate folder for processing. The following are suggested folder names.
If different folders are used, be sure to correct the `CONFIG` section of
subsequent scripts.

- `WD\Indexes\new_downloads_qq.txt` => `WD\Downloads\QQ`
- `WD\Indexes\new_downloads_itm.txt` => `WD\Downloads\ITM`
- `WD\Indexes\new_downloads_qm.txt` => `WD\Downloads\QM`
- `WD\Indexes\new_downloads_topo.txt` => `WD\Downloads\TOPO`

## Process

- Put topos in correct folder structure
- Convert GeoPDFs to GeoTIFFs

## Check

- Compare processed files with list and PDS library
- Get list of new (not updated) tif files (for updating mosaics)

## Document

- Update metadata

## Publish

### Update Libraries

- Copy pdf files to PDS
- Copy tiff files to PDS

### Update Mosaics

- Add new rasters to mosaics
- Update footprints with any new or updated metadata
  - Compare git history to see if metadata has changed

### Update repo/PDS documentation
