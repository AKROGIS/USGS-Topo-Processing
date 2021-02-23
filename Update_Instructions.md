# USGS Topo Map Processing Instructions

These instructions are for updating the USGS topographic map library
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

1. Clone (or refresh) the git repository to a working directory

   - <https://github.com/AKROGIS/USGS-Topo-Processing>
   - The working directory (e.g. `C:\tmp\topo`) is referred to as `WD` below.
   - The working directory should be on a fast local volume with 10s of free GB
     - Each map is at least 10MB, and there may be 1000 or more to process.
   - Check/Edit `working_folder` in the `CONFIG` object in
     `Tools\make_folders.py`
   - Check the other parameters in the `CONFIG` object.
   - Run the script `Tools\make_folders.py`to create working folders

2. Download the USGS database snapshot.

   - URL: <http://thor-f5.er.usgs.gov/ngtoc/metadata/misc/topomaps_all.zip>
   - Referencing web page (as of Nov. 2020):
     <https://www.usgs.gov/core-science-systems/ngp/tnm-delivery/topographic-maps>

3. Unzip the download to the `WD\Scratch` folder

   - There should be 3 files in this folder (1 readme, and 2 CSV files)

4. Check the check the `Change History:` at the end of `WD\Scratch\readme.txt`
   in the unzip folder for changes that might effect the scripts. For example
   adding or deleting columns in the data file.  If there have been changes,
   then any of the scripts below may fail.  If so, then the scripts will need
   to be updated to reflect the changes. In most cases, there is a `CONFIG`
   object at the beginning of the script that contains assumptions about the
   database. Most changes can be made per the comments in the `CONFIG` object.

5. Make the download lists

   - Check and update the `CONFIG` object at the beginning of
     `WD\Tools\make_alaska_lists.py`
   - Check the file containing the date of the last processing.
     - see `CONFIG`, but typically `Indexes\last_processing_date.txt`
     - If this file does not exist, then it is assumed NO topo file have been
       previously downloaded.
   - Run `WD\Tools\make_alaska_lists.py` to create the download lists and
     metadata records for the mosaics.

6. Check the metadata against PDS and download lists

   - Check and update the `CONFIG` object at the beginning of
     `WD\Tools\compare_pds_to_metadata.py`
   - Run `WD\Tools\compare_pds_to_metadata.py` to compare the PDS with the
     metadata files.
   - There should be no **Extra Files (in PDS but not metadata)**
   - Everything in **Extra Paths (in metadata, but not PDS)** except
     the paths in `Current_GeoTIFF` should be in one of the
     `WD\Indexes\new_downloads_*.txt` files.  If this is not the case, then
     something has gone wrong.  This problem should be investigated and
     resolved before continuing.
   - Possible sources of error include (by likelihood):
     - The `CONFIG` parameters in `WD\Tools\make_alaska_lists.py`.
     - Other assumptions in `WD\Tools\make_alaska_lists.py`.
     - Changes (deleting or renaming files) on the PDS since the last
       processing.
     - Changes in the structure or semantics of the USGS database

7. Update the repo.
   The previous step will update various files in the `WD\Indexes` folder
   This history is retained in the repository.  Use git (or GitHub app) to
   commit and push the changes. You can use the git commit log to see the
   dates and file lists of prior updates.

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
If different folders are used, be sure to correct the `CONFIG` section of
subsequent scripts.

- `WD\Indexes\new_downloads_qq.txt` => `WD\Downloads\QQ`
- `WD\Indexes\new_downloads_itm.txt` => `WD\Downloads\ITM`
- `WD\Indexes\new_downloads_qm.txt` => `WD\Downloads\QM`
- `WD\Indexes\new_downloads_topo.txt` => `WD\Downloads\TOPO`

## Process

1. Put topos in correct folder structure

   This will move the files in the various `WD\Download` folders to
   the PDS folder structure in `WD`

   - Check and update the `CONFIG` object at the beginning of
     `WD\Tools\organize_downloads.py`
   - Run `WD\Tools\organize_downloads.py` to move the files.

2. Find/Remove duplicate PDFs
   Sometimes USGS updates just the GeoPDF metadata, which makes it look like the
   map is new, when infact there is no change in the PDF contents.  First
   run `compare_file.py` to see if the downloaded PDFs are the same or different
   keep the different files and remove the duplicates.

3. Convert GeoPDFs to GeoTIFFs
  - run `create_gdal_batchfile.py`
  - run generated batch file (break into chunks)
  - run `add_pyramids.bat`

## Publish

### Update Libraries (Copy to PDS)

  Manually copy `WD` folders to PDS.  Current_GeoPDF should all be additive
  If there is a warning that you will be replacing files, stop and figure out
  why.  You may be replacing files in `Current_GeoTIF`, If so, there should be
  multiple GeoPDFs for this tile.  It is unlikely that there will be future
  changes to the `Historic` folders, so review any changes closely.

### Update Mosaics

- Generate list of new geotif raster compare download list to existing tif in
  the PDS.  Updated tiles do not require adding rasters (just metadata)
  - Add new rasters (if any) to mosaics
- Update footprints with any new or updated metadata
  - Compare git history to see if metadata has changed
  - Update manuallY??
  - what if there are new fields in downloaded CSV database?
  - how do we update just the changed values?  Manual??
  - we can match based on raster name
  - Do we need any attributes for the Current topos?
  - Historic topos are unlikely to change
    - handle small discret changes manually
    - large changes with kill and fill (bulk erase and update all attributes)

 - We will track `Scale`, `Map Folder`, `Create Date`, `PDS Path` and
   `Date on Map` from `all_metadate_topo.csv`
   where `Version` == `Current` (not `Historical`) 
   in `X:\Mosaics\Statewide\Charts\USGS_Topo_Maps.gdb\Current_1to25k`
   Link on the `Raster Name` == `Name`

 - Historical footprints are joined to the metadata with the following
   geoprocessing command.  If there is a major update, a similar command can
   be used to do a bulk update.  Minor changes (as seen in any changes to the
   metadata files in the git diff) will need to be done manually.  None are
   expected. Summary of command below: join mosaic with csv on `Name = Raster_Name`
   add all fields except `ObjectID` and `Raster_Name`

   ```Python
   arcpy.JoinField_management(in_data="C:/tmp/pds/topos/USGS_Topo_Maps.gdb/Historic_1to250k_Bathymetry", in_field="Name", join_table="C:/tmp/pds/topos/meta.gdb/all_metadata_qm", join_field="Raster_Name", fields="Series;Version;Cell_ID;Map_Name;Primary_State;Scale;Date_On_Map;Imprint_Year;Woodland_Tint;Visual_Version_Number;Photo_Inspection_Year;Photo_Revision_Year;Aerial_Photo_Year;Edit_Year;Field_Check_Year;Survey_Year;Datum;Projection;Advance;Preliminary;Provisional;Interim;Planimetric;Special_Printing;Special_Map;Shaded_Relief;Orthophoto;Pub_USGS;Pub_Army_Corps_Eng;Pub_Army_Map;Pub_Forest_Serv;Pub_Military_Other;Pub_Reclamation;Pub_War_Dept;Pub_Bur_Land_Mgmt;Pub_Natl_Park_Serv;Pub_Indian_Affairs;Pub_EPA;Pub_Tenn_Valley_Auth;Pub_US_Commerce;Keywords;Map_Language;Scanner_Resolution;Cell_Name;Primary_State_Name;N_Lat;W_Long;S_Lat;E_Long;Link_to_HTMC_Metadata;Download_GeoPDF;View_FGDC_Metadata_XML;View_Thumbnail_Image;Scan_ID;GDA_Item_ID;Create_Date;Byte_Count;Grid_Size;Download_Product_S3;View_Thumbnail_Image_S3;NRN;NSN;Map_Folder;AWS_URL;PDS_Path")
   ```
To recreate the footprints.
* Create a new mosaic - See original processing for details
  - Add Rasters
  - Fix footprints
  - Add columns from manual inspections (`Indexes\*_data.csv`)
* Add columns from USGS (`Indexes\all_metadata_*.csv`)
  - Add CSV file to a geodatabase
  - Use Join Fields GP tool
  - Join on `Mosaic.Name` = `CSV.Raster_Name`
  - Exclude at least fields `OBJECTID` and `Raster_Name` (more for current topo)

To update all the manual or USGS Columns
* Use Delete Fields GP tool to remove all columns to the right
  - Starting with `Series` and `Version` for USGS data
  - Starting with columns after `UriHash` for manual data
* Use `Join Fields` GP Tool as above to add attributes as above.

To add data to just the new topo rasters, create a limited CSV from
`Indexes\all_metadata_*.csv` that has only the records for the new rasters
try filtering by `Create Date` or matching on the download list.  Then follow
the instructions above for `Join Fields`, but only select the fields that are
already in the footprints

### Update repo/PDS documentation

## Verify

- Run `WD\Tools\compare_pds_to_metadata.py` again.  The output should be

    ```
    Woot, Woot!, No Extra Paths
    Woot, Woot!, No Extra Files
    ```

- If not, check that all the files `WD\Current*` and `WD\Historic*` were copied
  to the PDS.
- If that is not the problem, then I'm sorry, but you are in unexpected
  territory and you will need to troubleshoot the problem on your own. See the
  suggestions above in Step 6 of the *Discover* section.

- New script to check footprints in mosaics with the list of files in the PDS
  1) missing footprints for existing rasters
  2) broken links: missing rasters for existing footprints.

## Document

- Commit changes to repo
  - new download date
  - updated metadata files and download lists
- Update publish date in mosaic metadata


# TO DO

- Add CSV metadata attributes mosaic footprints
- Create properly filtered ITM mosaic
- Create metadata (Item description) for mosaics
- Create Layer files
- Publish layer files in TM
- Cleanup Python code to match current conventions
  - import csv23.py
  - use Config class and not CONFIG dict.
- Finish this document
- Rename `arrange_topos.py` to `organize_downloads.py`
  - Fix code.  It should move files from `WD\Download` folders to
    a `WD` folder that matches the PDS (See discussion above)
  - Finish code and test
- Cleanup `create_gdal_batchfile.py` script
  - build from columns in metadata and files in `WD\CurrentGeoPDF` folder
- Fix/Test mosaic scripts
  1) add new rasters to mosaic (`build_mosaics.py` -> `add_rasters_to_mosaics.py`)
  2) update raster mosaic footprint attributes from metadata files.
- New script to check mosaic footprints with PDS raster files  (see discussion above)
- Move `compare_trees.py` to misc scripts
- Rename `pdf_diff.py` to `compare_files.py` and document above (process step 2)
- rename andthis folder and reclone the repo
- Test all the scripts with Python 2 and 3 (Repo should not change)
- Run the process from start to finish with latest database download

