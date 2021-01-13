# US Topo Update Instructions (obsolete)

This document describes the initial update process.  It has since been replaced
by [Update Instructions](Update_Instructions.md)

* Get the last update from the end of the file
  `X:\Extras\AKR\Statewide\Charts\USGS_Topo\Indexes\nationalmap_search_results_pdf_YYYYMMDD.csv`
  with the most recent date
* Open <https://viewer.nationalmap.gov/basic/>
  * Click `Datasets` tab
  * Select `US Topo` under the `Maps` section
  * Click on `Advanced Search Options`
    * Select `Date Range`
    * For Data Type, select `Last Update` in the pick list
    * Start Date = last update date from above
    * End Date = today
  * Zoom/Pan map (and change browser aspect ration) so that **ALL** of Alaska
    is visible, and **NO** other states are visible.
  * CLick the big `Find Products` button.
  * Click the `Save as CSV` Button
    * Save as lastupdateYYYYMMDD.csv
* click `Return to Search` button
  * Change Data Type, select `Date Created` in the pick list
  * Click the big `Find Products` button.
  * Click the `Save as CSV` Button
    * Save as createdYYYYMMDD.csv
* compare/merge two download files to make a single unique list
  * Large files are easiest to check by importing to SQL server
  * Smaller files can be opened in Excel and compared.
  * A cheat is to just select hte file with more records
  * or Open the two files and compare with windiff
  * or make the uget list for both files and compare with windiff
* Make Uget list
  * Copy `X:\Extras\AKR\Statewide\Charts\USGS_Topo\Tools\make_uget_list.py` to a working directory
  * Edit `make_uget_list.py` line 10 to use the input path from above
  * Run `make_uget_list.py` with Python2.7
    * If there is an error,  make sure there is no empty line at the end of the file.
  * Run it again with other download list
  * Change the file names to .csv
  * open in Excel, sort, and delete duplicates then save
  * rename to *.txt

* Download larger of the two uget lists
* Run merge_unique_uget.py to get a list of files in 2nd, but not first uget list
* Download the third uget list
* Compare the downloaded files with the X drive files to find which are new/dups/updates
* run `remove_dups.py` to remove the dups.
* put the downloaded pdfs in a `Current_GeoPDF` folder
* create a `Curent_GeoTIFF` folder adjacent to the `Current_GeoPDF`
* Run `arrange_topos.py`
* run `create_gdal_batchfile.py`
* break into 8 equal chunks
* open a new command prompt
  * run `c:\users\resarwas\gdal3\sdkShell.bat`
  * cd to folder with batch file
  * run batch file
* repeat for all 8 batch files
  * each batch file will take about 5-15 minutes per line. if there are only a few files to process, then fewer batch files may be better.
* when done, close all but one command window
* In the remaining command window run `add_pyramids.bat`
  * takes about 5 seconds per file to finish.
* Run `compare_trees.py` on X:\....\GeoPDF and working GeoPDF folders
* Run `compare_trees.py` on X:\....\GeoTIFF and working GeoTIFF folders to get a list of duplicates
  * use this list to make a list of filepaths as input to the next step
  * needs a header line for the next step (see IFSAR processing instructions)
* copy, edit and run `pds-reorg\build_mosaics.py` to add new files to mosaic

* If new topos were added (skip if only changes were updated topos)
  * repair footprints
    * footprints of newly added rasters will include the entire image, which includes
      the white area around the image for the marginalia.  This step will set
      the footprint of each raster to the extents of the map content in the image.
    * Right click, Modify->Import Footprints or Boundary...
      * target: Footprints
      * Target Join Field: Name
      * Input: `Indexes\MAPINDICES_Alaska_State_GDB.gdb\Cells\CellGrid_7_5minute`
      * Input Join Field: cell_name
  * Update boundary
    * Must be done after the footprints have been repaired.
    * In ArcCatalog, right click on mosaic, select Modify -> Build Boundary...
  * fix maxPS
    * In ArcMap, edit the footprints and set `MaxPS = 40` for all source tiles.
      This will set a scale of 1:151,181 to switch from overviews to source
      tiles. A larger HighPS is possible due to the internal pyramids, but that
      will require loading too many source tiles when zoomed out.
  * Update Overviews
    * If you made a copy, fix the paths of the writable copy of the overviews
      * right click, `Modify` -> `Repair...` and replace the X drive path to the
        overviews to the writable copy.
    * You cannot Define and Build overviews in one step,  because despite the options
        to only updated the stale and new it will recreate all.
    * Define Overviews
      * **Do not** use `Optimize` -> `Define Overviews...` in the context menu
      * Use `Optimize` -> `Build Overviews...` in the context menu with the
        following options:
      * Define Missing Overview Tiles (optional): ON
      * Generate Overviews (optional): OFF
      * Generate Missing Overview Images Only (optional): ON
      * Generate Stale Overview Images Only (optional): ON
      * The second two will be grayed out, when the second option is off,
        but I think they still apply.
    * Use ArcMap to find existing overviews that need to be updated
      * Use the graphic selection tool to Select the area of the new tiles.
        This may need to be multiple selections. Be sure to get right up to the edge
        of the existing tiles (the edge of some overviews may be very close to a base tile)
        * A trick is to select all the new (non overview) raster, and export to a separate feature class.
          Then unselect, and select all of the old overviews. If this is not easy to
          do in the attribute table, do it by "select by attribute" where name like 'Ov%' and
          Category <> 3. Then select by location, from the selected set the footprints
          that intersect the exported FC of new raster footprints.
      * Start an edit session.
      * Open the attribute table, and filter to only selected features.
      * The features should be in OID order. Scroll from the bottom (New overviews last, new
        base tiles next).  Any overviews selected above that should be highlighted.
        Do not highlight any base tiles (check the name).
      * Click the button to reselect the highlighted tiles.  Only the old overviews that overlap
        the new base tiles should now be selected.
      * right click on the Category column header, and Calc the field to set Category = 3.
      * Save edits and close ArcMap
    * Build Overviews for new overviews
      * Use `Optimize` -> `Build Overviews...` in the context menu with the
        following options:
      * Query Definition (optional): `Category = 3`
      * Define Missing Overview Tiles (optional): OFF
      * Generate Overviews (optional): ON
      * Generate Missing Overview Images Only (optional): ON
      * Generate Stale Overview Images Only (optional): ON
    * Copy new overviews to the server
      * Check the file count.  IN many cases, there are mask files that are
        deleted in the local copy, and they need to be deleted from the server
        overview folder.
    * right click, `Modify` -> `Repair...` and replace the C drive path to the
        overviews to X drive overviews.
    * delete or rename the C drive overview folder, and test the mosaic.
      If all is well, then copy mosaic GDB to the server.

Initially need to add some columns

* Right click on mosaic in ArcCatalog and select Properties...
* Click on Fields tab and add 4 columns
  * CreateDate * Date
  * MapYear * Source Integer
  * SourcePDS * text(300)
  * SourceAWS * text(300)
