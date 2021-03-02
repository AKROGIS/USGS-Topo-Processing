# USGS Topo Map Processing Instructions

These instructions are for updating the USGS topographic map library
and raster mosaics maintained in the Alaska GIS PDS.  The process is to
look for changes made by the USGS since the last time this process was
run and then update the published products accordingly.

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

1. Clone (or refresh) the git repository to a local working directory

   - Use GitHub desktop application or the git command line to clone
     <https://github.com/AKROGIS/USGS-Topo-Processing> to a working directory.
   - The working directory is referred to as `WD` in the instructions below.
   - The working directory should be a fast local volume with 10s of free GBs.
     - Each map is at least 10MB, and there may be a 1000 or more to process.
   - The scripts assume the `WD` is `C:\tmp\USGS-Topo-Processing`. If you cloned
     the repo to a different location, then either move it, or edit the `Config`
     properties in all the scripts in `WD\Tools`.
   - Run the script `WD\Tools\make_folders.py` to create working folders in
     the cloned repo.

2. Download the USGS database snapshot.

   - URL: <http://thor-f5.er.usgs.gov/ngtoc/metadata/misc/topomaps_all.zip>
   - Referencing web page (as of Feb. 2021):
     <https://www.usgs.gov/core-science-systems/ngp/tnm-delivery/topographic-maps>

3. Unzip the download to the `WD\Scratch` folder

   - There should be 3 files in this folder (1 readme, and 2 CSV files)

4. Check the `Change History:` at the end of `WD\Scratch\readme.txt`
   for changes that might effect the scripts. For example
   adding or deleting columns in the data file.  If there have been changes,
   then any of the scripts below may fail.  If so, then the scripts will need
   to be updated to reflect the changes. In most cases, there is a `Config`
   object at the beginning of the script that contains assumptions about the
   database. Most changes can be made per the comments in the `Config` object.

5. Make the download lists

   - Check and update the `Config` properties at the beginning of
     `WD\Tools\make_alaska_lists.py`
   - Check the file containing the date of the last processing.
     - see `Config`, but typically `WD\Indexes\last_processing_date.txt`
     - If this file does not exist, then it is assumed NO topo file have been
       previously downloaded. If it is missing it can be recreated.  The content
       looks like `2021-02-23`
   - Run `WD\Tools\make_alaska_lists.py` to create the download lists and
     metadata records for the mosaics.

6. Check the metadata against PDS and download lists

   - Check and update the `Config` properties at the beginning of
     `WD\Tools\compare_pds_to_metadata.py`
   - Run `WD\Tools\compare_pds_to_metadata.py` to compare the PDS with the
     metadata files.
   - There should be no **Extra Files (in PDS but not metadata)**
   - Everything in **Extra Paths (in metadata, but not PDS)** except
     the paths in `WD\Current_GeoTIFF` should be in one of the
     `WD\Indexes\new_downloads_*.txt` files.  If this is not the case, then
     something has gone wrong.  This problem should be investigated and
     resolved before continuing.
   - Possible sources of error include (by likelihood):
     - The `Config` properties in `WD\Tools\make_alaska_lists.py` are wrong.
     - Other assumptions in `WD\Tools\make_alaska_lists.py` are wrong.
     - Changes (deleting or renaming files) on the PDS since the last
       processing.
     - Changes in the structure or semantics of the USGS database.

7. Update the repo.

   The previous step will update various files in the `WD\Indexes` folder
   This history is retained in the repository.  Use git (or GitHub app) to
   commit and push the changes. You can use the git commit log to see the
   dates and file lists of prior updates.

   It appears that the order of the maps in the USGS download is not consistent
   so there may be some changes in the `WD\Indexes\all_metadata_*.csv` files
   that is just the order of select lines.  These changes can be ignored (you
   do not need to copy to the PDS, or commit to the repo.)

8. Done?

   If all the the files `WD\Indexes\new_downloads_*.txt` are empty, you are
   done! Otherwise, continue on.

## Download

The previous step generated several lists of download URLs for new/updated
topo maps.  These lists can be used to download individual files in a web
browse, or automated with uGET, curl, or a custom script.  These instructions
assume you are using [uGET](https://sourceforge.net/projects/urlget/)
which is an application that does not require admin permissions.  See the
[USGS uGET page](https://viewer.nationalmap.gov/uget-instructions/)
for additional instructions on installing and using uGET (ignore the
instructions for "Preparing Input Text File" as that was done in the previous
step).

Each of the download lists (if not empty) should be downloaded to a
separate folder for processing. The following are suggested folder names.
If different folders are used, be sure to correct the `Config` properties of
subsequent scripts.

- `WD\Indexes\new_downloads_qq.txt` => `WD\Downloads\QQ`
- `WD\Indexes\new_downloads_itm.txt` => `WD\Downloads\ITM`
- `WD\Indexes\new_downloads_qm.txt` => `WD\Downloads\QM`
- `WD\Indexes\new_downloads_topo.txt` => `WD\Downloads\TOPO`

## Process

1. Find/remove duplicate PDFs

   **This must be done before the next step because it assumes the files are
   still in the `WD\Downloads\TOPO` folder.**

   Sometimes USGS updates just the metadata for a GeoPDF. This makes it look
   like an updated map, so we download it, only to find out the map content is
   unchanged.  This step identifies any of the downloaded GeoPDFs that have not
   actually changed.

   - Check and update the `Config` properties at the beginning of
     `WD\Tools\compare_file.py`
   - Run `WD\Tools\compare_file.py` to identify the duplicate files.
   - Delete all files in `WD\Downloads\TOPO` that the script output marks with
     `dup:`; keep all files marked with `update:` or `new:`. If there are a lot
     of intermixed files to delete, copy/paste the output into a text editor and
     search and replace `dup:` with `delete `, `new:` with `REM ` and `update:`
     with `REM `, then save as a `*.bat` file and execute in the
     `WD\Downloads\TOPO` folder.

2. Put topos in the correct folder structure

   This will move the files in the various `WD\Download` folders to
   the PDS folder structure in `WD`.  This will make it easier to copy to the
   PDS.

   - Check and update the `Config` properties at the beginning of
     `WD\Tools\organize_downloads.py`
   - Run `WD\Tools\organize_downloads.py` to move the files.

3. Convert GeoPDFs to GeoTIFFs

    This step will create a GEOTIFF for each of the new GeoPDFs and then add
    overviews to all new GeoTIFFs.

   - Check and update the `Config` properties at the beginning of
     `WD\Tools\create_gdal_batchfile.py`
   - Run `WD\Tools\create_gdal_batchfile.py` to create a GDAL batch script.
   - Open the output script in a text editor and determine how many lines are
     in the file.  Each line will take about 5-15 minutes to execute.  If the
     file is short, or you have a lot of time, you can run the file as is,
     otherwise, you can break the file into n evenly sized chunks, where n is
     the number of CPUs/cores on your computer. Each chunk can be run
     concurrently in a separate DOS command window to speed up the processing.
   - To run the GDAL batch script you will need to open a DOS command window, or
     a Windows Power Shell.  Before you can execute the GDAL Batch script, you
     need to execute `SDKShell.bat` in the `GDAL` installation folder.
   - After all portions of the GDAL batch script are done executing, you should
     have the same number of new GeoTIFFs in `WD\Current_GeoTIFF` as there are
     new GeoPDFs in `WD\Current_GeoPDF`.
   - Open a CMD window and execute `SDKShell.bat` in the `GDAL` installation
     folder (or use the command window from the previous step).
   - In the command window, change directory (`cd`) to `WD\Current_GeoTIFF`
   - In the command window, execute `WD\Tools\add_pyramids.bat`

## Publish

### Update Libraries (Copy to PDS)

  Manually copy the folders `WD\Current_GeoPDF`, `WD\Current_GeoTIFF`,
  `WD\Historic_ITM`, `WD\Historic_QM`, `WD\Historic_QQ`, and `WD\Indexes`
  to the PDS (`X:\Extras\AKR\Statewide\Charts\USGS_Topo`). You can skip a folder
  if it is empty.  **IMPORTANT** The contents of the local folders is incomplete
  and needs to be _merged_ with the existing content on the PDS.  Do not delete
  or replace the PDS folders with these local folders.

  `Current_GeoPDF` should all be additive. If there is a warning that you will
  be replacing files, stop and figure out why.  You may be replacing files in
  `Current_GeoTIF`, If so, there should be multiple GeoPDFs for this tile.  It
  is unlikely that there will be future changes to the `Historic` folders,
  so review any changes closely.

  Be sure to update the PDS change log!

### Update Mosaics

If there are new (not updated) rasters, then these will need to be added to the
mosaic.  If there are other changes to the metadata, the the footprint
attributes will need to be updated.

#### Adding New Rasters

It is possible that all of the downloaded rasters are just updates to existing
cells that are already in the mosaic. Use `compare_mosaics_to_pds.py` to see
if there are rasters in the PDS that are not in the mosaic ("unused rasters").

- Check and update the `Config` properties at the beginning of
  `WD\Tools\compare_mosaics_to_pds.py`. I recommend checking all mosaic without
  creating a CSV to see if there are any changes.
- Run `WD\Tools\compare_mosaics_to_pds.py` to see if there are rasters to add.

If there are changes you are done.  Otherwise, continue

- Edit the `Config` properties to create CSV files and rerun.
  You comment out the mosaics that do not have any changes.
- Copy the mosaic from the PDS to a local work area.
- Check and update the `Config` properties at the beginning of
  `WD\Tools\add_rasters_to_mosaics.py`. In particular, make sure that the CSV
  filenames are correct and the mosaic path is the local copy.
- Run `WD\Tools\add_rasters_to_mosaics.py` to add the missing rasters.

The new rasters will need to have the footprints clipped to the map content
area. The following instructions are for the current topos.  for the historic
topos, see the [Initial Processing Instructions](Initial_Process_Instructions.md)

- In ArcCatalog browse to the local copy of `Current_1to25k` mosaic.
- Right click, select `Modify`->`Import Footprints or Boundary...`
  - target: `Footprints`
  - Target Join Field: `Name`
  - Input: `Indexes\MAPINDICES_Alaska_State_GDB.gdb\Cells\CellGrid_7_5minute`
  - Input Join Field: `cell_name`

The new footprints need additional attributes contained in the
`Indexes\all_metadata_*.csv` files.  Currently there is no easy way to update
just the new footprints, so a kill and fill strategy as described below is
recommended.

The overviews may need to be updated (only for the current topos) if there
is a noticeable increase in the extents of the current coverage. (If
existing topos are updated, this does not require updating the overviews.)
See the readme files for the IFSAR mosaics
(X:\Extras\AKR\Statewide\DEM\SDMI_IFSAR\_README) for details on how
to update the overviews without regenerating all the overviews (to
minimize the burden on robocopy)

#### Updating Footprint Attributes

If new footprints were added to a mosaic, or if the metadata for existing
footprints has been updated (which can be determined by the git change detection)
you will need to update the footprint attributes in the mosaics.

While it is possible to join the `Raster Name` attribute in the
`Indexes\all_metadata_*.csv` files to the `Name` attribute in the mosaic
footprints, and the do some field calculations to update selected records as
needed, this is likely more tedious that simply deleting all the extra
attributes, and then re-adding them, as described below.

##### Current Topos

- Use the `Delete Fields` GP tool to remove all columns after the `UriHash`
  attribute.
- Use `Join Fields` GP Tool to add attributes:
  - Import `Indexes\all_metadata_topo.csv` into a scratch geodatabase to create
    a geodatabase table.
  - Join on the `Name` attribute in the footprints and the `Raster_Name`
    attribute in the CSV data.
  - Exclude at least fields `OBJECTID` and `Raster_Name`
  - Add at least these attributes: `Scale`, `Map Folder`, `Create Date`,
    `PDS Path`, `AWS URL` and `Date on Map`
  - Click `OK` to add the columns and data.

##### Historic Topos

Fortunately, these are unlikely to change, and it is possible that even if
changes occur, they can be ignored.

There are two parts to the historical footprint attributes:

1) The locally and manually maintained files `Indexes\*_data.csv`
2) The USGS metadata `Indexes\all_metadata_*.csv`

These instructions are for replacing both sets of attributes, however they
can be adapted to replacing just one or the other. The example is for the
`ITM` mosaic only, `QM` and `QQ` are similar.

- Use the `Delete Fields` GP tool to remove all columns after the `UriHash`
  attribute from `Historic_1to63360_All`.
- Use `Join Fields` GP Tool to add attributes from the local data:
  - Import `Indexes\itm_data.csv` into a scratch geodatabase to create
    a geodatabase table.
  - Join on the `Name` attribute in the footprints and the `Raster`
    attribute in the CSV data.
  - Exclude at least fields `OBJECTID` and `Raster`
  - Click `OK` to add the columns and data.
  - Import `Indexes\all_metadata_itm.csv` into a scratch geodatabase to create
    a geodatabase table.
  - Join on the `Name` attribute in the footprints and the `Raster_Name`
    attribute in the CSV data.
  - Exclude at least fields `OBJECTID` and `Raster_Name`
  - Click `OK` to add the columns and data.
- Repeat this process for the other `Historic_1to63360_*` mosaics, or
  create the other `Historic_1to63360_*` mosaics from `Historic_1to63360_all`
  as detailed in the
  [Initial Processing Instructions](Initial_Process_Instructions.md)

#### Publishing Mosaics

- Update publish date in mosaic metadata
- Publish the local working mosaic database to the PDS

## Verify

- Run `WD\Tools\compare_pds_to_metadata.py` again.  The output should be

    ```sh
    Woot, Woot!, No Extra Paths
    Woot, Woot!, No Extra Files
    ```

- If not, check that all the files `WD\Current*` and `WD\Historic*` were copied
  to the PDS.
- If that is not the problem, then I'm sorry, but you are in unexpected
  territory and you will need to troubleshoot the problem on your own. See the
  suggestions above in Step 6 of the *Discover* section.
