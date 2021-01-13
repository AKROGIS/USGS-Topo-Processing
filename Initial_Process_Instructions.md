# Processing Notes

This document describes how the initial set of files was downloaded and
prepared for the PDS.  It has continued value, because it identifies the files
that required special consideration because they did not match the norm, or
were incorrectly described by USGS.

## Current Topos (1:25k maps)

1) Search the national map to create a download list
   - This is more difficult than necessary, because the search list download is
     limited to 5000 records.  For the initial search, I created extents
     rectangles for different parts of the state, and then merged the results
     and removed duplicates (i.e. tiles that touched the extents and thus were
     included in multiple search results) and sort by title
   - Search Filter: SubCategory: US Topo Current; Data Extent: 7.5x7.5 minute;
     File Format: GeoPDF/Geospatial PDF
2) Download using a simplified list and uget (or curl)
   - Create the URL list with `make_uget_list.py`.  Check/edit the beginning of
     the script to ensure the correct input/output file name are specified.
   - Launch `uget` (search Google for download of app - can be run from
     anywhere; no need to install). In file menu, under batch mode load text
     import file.
3) Organize into folders
   - Run `arrange_topos.py` which will move all files in `Current_GeoPDF` into
     the appropriate sub folder based on the root name of the file.  It will
     create sub-folders as necessary.  It is safe to run multiple times.
4) Compare file system to search results
   - Run `compare.py`, but fist check/edit the default paths at the beginning
     of the script.
5) Create GeoTIFFs from GeoPDFS
   - Run `create_gdal_batchfile.py`, but check/edit the configuration settings
     at the beginning of the script.
     - You will need to create a writable output folder i.e. `Current_GeoTIFF`
       first, but the script will create all necessary sub-folder.
     - The script will add a line to the output batch file for all missing PDF
       files without a matching TIFF file that is newer than the PDF.
     - Run the resulting batch file in a GDAL command window.  New PDFs can
       take 5-15 minutes to process, so it may be beneficial to split the batch
       file in several equal sized chunks (to match the number of cores on your
       computer) and run several processes in parallel.
   - Run `add_overviews.bat` which will add internal overviews (i.e. pyramids)
     to all geoTIFF files.
6) Build Mosaic
   - in ArcCatalog, create a new Mosaic Dataset with Alaska Albers NAD83
     projection.
   - Right click, `Add Rasters...` and import all files in `Current_GeoTIFF`
   - Right click, Modify->Import Footprints or Boundary...
     - target: Footprints
     - Target Join Field: Name
     - Input: `Indexes\MAPINDICES_Alaska_State_GDB.gdb\Cells\CellGrid_7_5minute
     - Input Join Field: cell_name
   - In ArcMap, edit the footprints and set `MaxPS = 40` for all source tiles.
     This will set a scale of 1:151,181 to switch from overviews to source
     tiles. A larger HighPS is possible due to the internal pyramids, but that
     will require loading too many source tiles when zoomed out.
   - in ArcCatalog, mosaic properties, General tab, Source Type: Processed;
     Mensuration: Basic
   - in ArcCatalog, mosaic properties, default tab, default compression: jpeg
   - in ArcCatalog, mosaic properties, default tab, set maximum number of
     rasters to 50 (from 20). This allows more than 20 source tiles to be
     returned when zoomed out to 1:151k. More than 20 tiles may fit on a large
     monitor at this scale.
   - Right Click, Optimize->Define Overviews... PixelSize: 40; Overview Sampling
     Factor: 3
   - Right Click, Optimize->Build overviews (uncheck Define Missing Overviews)
   - Copy to the PDS, and repair all paths to point to the PDS
7) Future Maintenance
   - Search the national map for files newer than the last download
     - Same search filter as above, but using the advanced Search Options, set
       the `Last Update` Start Date > previous search.  Repeat for `Date
       Created`
   - Run `make_uget_list.py`, and download new maps
   - Some may only have newer metadata, so before doing lots of processing, use
     `pdf_diff.py` to check if the new files are actually different than
     existing files.
   - Merge the new search results with the old search results.
     - Run `merge_search_results.py`, but check/edit the configuration settings
       at the beginning of the script.
   - Organize new PDFs as above
   - Compare file system to search results as above
   - Create new GeoTIFFS as above
   - Merge files with X drive
     - updated TIFF tiles will over write existing tiles
   - Update mosaic
     - mosaic does not need to be edited for updates to existing tile
     - new source tiles will need to be added to the mosaic
       - see instructions above, including updating the overviews.
     - See the readme files for the IFSAR mosaics
       (X:\Extras\AKR\Statewide\DEM\SDMI_IFSAR\_README) for details on how
       to update the overviews without regenerating all the overviews (to
       minimize the burden on robocopy)

## Historic QM Quads (1:250k maps)

1) Search the national map for a list of all 1:250,000 scale historic topo maps
   - This is harder than it should be, because there are 4 map sizes to search,
     and two extents to search (both sides of the anti-meridian).
   - On the National Map viewer, Use the map to set the search extents by
     coordinates (min long: -180, max long: -127, min lat: 49, max lat: 72). On
     the left side panel, select the Datasets tab, and then Historical
     Topographic Maps.  Below that, filter the list to 1x4 degree, and click
     Find Products.  Download the search results as a CSV file.  Repeat for the
     1x3, 1x2, and 1x1 degree map sizes.  And then again with extents of (min
     long: 160, max long: 180, min lat: 49, max lat: 72) for all 4 map sizes.
   - The 8 possible CSV files can then be merged, sorted, uniquified (Excel can
     do the uniquify on the merged CSV file) and sort by title.
   - As of 2018-12-09, this is the count of files available:
      - Western Hemisphere, 1x1:   3
      - Western Hemisphere, 1x2: 312
      - Western Hemisphere, 1x3: 945
      - Western Hemisphere, 1x4:  20
      - Eastern Hemisphere, 1x1:   0
      - Eastern Hemisphere, 1x2:  33
      - Eastern Hemisphere, 1x3:   0
      - Eastern Hemisphere, 1x4:   0
      - Dups: 7 maps for Rat Island, and 10 for Gareloi are in the 1x2 set in
        both hemispheres
2) Download using a simplified list and curl or uget
   - Create the URL list with `make_uget_list.py`.  Check/edit the beginning of
     the script to ensure the correct input/output file name are specified.
   - Launch `uget` (search Google for download of app - can be run from
     anywhere; no need to install)  in file menu, under batch mode load text
     import file.
   - compare download list to filesystem (`compare.py`)
3) Describe/Categorize each file.
   - Start by creating a file called `qm_data.csv` by using `list_topos.py`.
     Check and edit the configuration settings at the top of the script. This
     will create a CSV with the filename, and each constituent part of the
     filename as an attribute.
   - Manually reviewed each images to confirm the attributes, and add other
     attributes like revision date, print date, map series, etc. to help
     categorize the 10 or so versions of each map. Edits in `qm_data.csv`
   - Edits in `qm_data.csv` to manually selected the best version in each
     series. Usually it was the most recent, if there are dups by date, then
     the "best" color quality was chosen.
4) Loaded `qm_data.csv` into SQL server and ran several QC queries
   (`check_qmtopos.sql`) on the data (and made the appropriate corrections to
   `qm_data.csv`)
5) Build Mosaics
   - Create a new mosaic called Historic_1to250k with an Alaska Albers (NAD83)
     spatial reference system
   - Right click, `Add Rasters...` and import all files in `Historic_QM`
   - Load `qm_data.csv` into a FGDB table (the next step doesn't work on
     a table without an OID field). Delete this table after the next step
     to avoid confusion on the authoritative version.
   - Use ArcToolbox -> Data Management Tools -> Joins -> Join Field to join all
     attributes in `qm_data.csv` to Historic_1to250k footprints
      - Input Table: `Historic_1to250k`
      - Input Join Field: `Name`
      - Join Table: (temp table built from `Indexes\qm_data.csv`)
      - Output Joint Field: `raster`
      - Join Fields: All except `objectid`, `raster` and `file`
   - Since the rasters are in NAD27, we need to tell the mosaic to use the
     NADCON_Alaska transformation. This is in the mosaic properties near the
     bottom of the Defaults tab (Geographic Coordinate System Transform)
   - Also set the following Mosaic Properties:
      - General tab, Source Type: Processed; Mensuration: Basic
      - default tab, default compression: jpeg
   - Right click, Modify->Import Footprints or Boundary...
     - target: Footprints
     - Target Join Field: `Cell_Name` (from `qm_data.csv`)
     - Input: `Cell_PolygonsAll_as_NAD27` (as defined below)
     - Input Join Field: cell_name
   - duplicate mosaic several times and create specialty rasters with only the
     best in a series. i.e. remove rasters with a Query Definition of
     `best_topo = 0` or `best_bath = 0` or `best_mil = 0` or `best_sr = 0`
   - Create overviews
     - Edit the MaxPS for the Source tiles to match the MinPS of the first
       level of overviews.

## Historic Quarter Quads

Same process as for QM Quads above, except as noted below.

- Searching is easier, there are no quads on the far side of the anti-meridian,
  there is only one scale, and there are less than 5000, so all the results can
  be returned in one go.
- There are two maps (documented in `qq_data.csv`) that are mis-
  labeled, and mis-georeferenced.  The file name and the
  georeferencing match, but the file content is wrong.  USGS has
  been notified.  Regardless, these maps would not be chosen for
  display in the best of category.  I have fixed the cell name in `qq_data.csv`
  and the georeferencing, so these files will appear in the correct location.
  - Fairbanks D-3 SW_353673
  - Anchorage A-7 NE_353583
- Set MaxPS to 40 for source tiles, and set MinPS to 40 for overviews (same
  as the Current_GeoTIFFs at the same scale).  Also return up to 50 tiles.

## Historic Quad Maps

Same process as for QM Quads above, except as noted below.

- Need to break the state up into 3 areas as there are nearly 10,000
  results, and we can only download 5000 at a time (it is to difficult
  to divide the state evenly).
- Just search for GeoTiffs. Lake Clark C-4 has a GeoPDF and a GeoTIFF,
  and we only want the GeoTIFF.
- The following maps have incorrect georeferencing.  Most are correct at the
  lower right corner, but slightly too small.  The ArcGIS georeferencing Tools
  was used to create a new aux file and twfx (the mosaic uses only the aux file)
  - AK_Anchorage B-6_463478_1960_63360_geo
  - AK_Baird Inlet A-7_354117_1954_63360_geo
  - AK_Baird Inlet C-2_463533_1954_63360_geo
  - AK_Baird Inlet C-4_463534_1954_63360_geo
  - AK_Bethel D-8_353648_1954_63360_geo
  - AK_Cape Mendenhall D-4_354801_1952_63360_geo
  - AK_Cape Mendenhall D-4_354802_1952_63360_geo
  - AK_Cordova A-7 and A-8_355133_1988_63360_geo
  - AK_Cordova A-7 and A-8_355134_1951_63360_geo
  - AK_Cordova A-7 and A-8_355135_1951_63360_geo
  - AK_Cordova A-7 and A-8_355136_1953_63360_geo
  - AK_Cordova B-4_355151_1951_63360_geo
  - AK_Cordova B-4_355152_1951_63360_geo
  - AK_Harrison Bay B-3_463763_1962_50000_geo
  - AK_Hooper Bay D-3_356089_1953_63360_geo
  - AK_Hooper Bay D-3_356090_1953_63360_geo
  - AK_Iliamna B-2_356239_1958_63360_geo
  - AK_Iliamna B-2_356240_1958_63360_geo
  - AK_Iliamna B-2_356241_1958_63360_geo
  - AK_Kenai B-7_356602_1958_63360_geo
  - AK_Kenai B-7_356603_1958_63360_geo
  - AK_Mount Saint Elias A-6_357849_1985_63360_geo
  - AK_Nunivak Island C-1_358208_1954_63360_geo
  - AK_Seward C-4_464099_1952_63360_geo
  - AK_Skagway B-8_359217_1961_63360_geo
  - AK_Skagway B-8_359218_1961_63360_geo
  - AK_Stepovak Bay C-5 and C-6_359335_1963_63360_geo
  - AK_Stepovak Bay C-5 and C-6_359336_1963_63360_geo
- The following maps have the incorrect name (so they got the wrong clipping
  footprint, and 3 of the four are goereferenced to the location of the
  incorrect name.  The cell name in `itm_data.csv` was corrected, and where
  necessary, the file was correctly georeferenced as above.
  - AK_Baird Mountains D-3_354191_1955_63360_geo is actually D-4
  - AK_Bering Glacier A-4_354369_1984_63360_geo is actually A-6
  - AK_Bradfield Canal A-1_354709_1997_63360_geo is actually A-5
  - AK_Bradfield Canal A-1_354711_2000_63360_geo is actually B-6
  - AK_Candle A-2_354754_1955_63360_geo is actually A-3
  - AK_Dillingham D-2_355444_1954_63360_geo,tif is actually C-2
  - AK_Hagemeister Island D-5_355868_1950_63360_geo is actually D-6
  - AK_Juneau D-3_356368_1949_63360_geo is actually D-4
  - AK_Kantishna River D-5_356458_1953_63360_geo is actually D-4
  - AK_Mt Hayes A-1_357859_1949_63360_geo is actually A-4
  - AK_Mt Hayes D-1_357866_1950_63360_geo is actually D-4 (georef ok)
  - AK_Mt Hayes D-1_357867_1950_63360_geo is actually D-4 (georef ok)
  - AK_Mt Katmai B-5_357875_1951_63360_geo.tif is actually D-5 (georef ok)
  - AK_Selawik D-6_358774_1952_63360_geo is actually Seward D-6
  - AK_Sumdum D-4_359404_1960_63360_geo is actually D-5
  - AK_Talkeetna C-2_359560_1958_63360_geo is actually Talkeetna C-3
- Set MaxPS = 50 for source tiles and MinPS = 50 for overviews

## Historic Footprints

The Historic topos need clipping footprints. Some of those footprints need to
be altered from the simple rectangular shape to include the bleed into the
marginalia that occurs on some maps.  Furthermore, the clipping footprints
need a special hack on the Spatial Reference System to accommodate the NAD27
to NAD83 mismatch. The mosaic will be in NAD83, but the source tiles will be
in NAD27.  In order for the footprints to work correctly (discovered through
trial and error) is for the defined spatial reference system to be NAD83, but
the actual geometry be for the NAD27 boundaries.  The source footprints are in
NAD83.

1. Copy the Cell_PolygonAll layer from MAPINDICES_Alaska_State_GDB.gdb to a new
   empty FGDB (`Indexes\NPS_Processing_Data.gdb`).
2. Remove all Cells with `Cell_Size = 1`.  These are 3.75x3.75 minute cells
   which we do not have in Alaska, especially for historical maps.
   - Cell_Size = 2 (7.5 minutes) will be used for historical_QQ
   - Cell_Size = 4 (15 minutes) will be used for historical_ITM
   - Cell_Size = 7-10 (1 to 4 degrees) will be used for historical_QM
3. The polygons are in NAD83, redefine the projection as NAD27.  REDEFINE not
   re-project, using the ArcTool Box -> Data Management Tools -> Projections and
   Transformations -> Define Projection
4. Re-project the NAD27-defined data to NAD83 with the NADCON-Alaska
   transformation. Using the ArcTool Box -> Data Management Tools ->
   Projections and Transformations -> Project.  Save the result as
   Cell_PolygonAll_as_NAD27
5. Edit the footprints to match the overflow, this is most easily done
   by adding the original images to a map with the footprints.  Be sure
   to set the NADCON_Alaska Transformation.  The following cells have
   altered footprints.  Note that some may have a WGS84 version (see section 6
   below)
    - Historic QQ
      - Saint George Island East
      - Saint Paul Island East
      - Yakutat C-5 SW
    - Historic QM
      - Chignick
      - Gareloi
      - Ketchican
      - Port Moller
      - Sutwick
      - Unalaska
    - Historic ITM
      - Afognak D-1
      - Baird Inlet A-7
      - Bering Glacier A-8
      - Black B-1 and A-2
      - Bradfield Canal C-5
      - Bristol Bay A-2 and B-1
      - Cape Mendenhall D-4
      - Chignik B-7
      - Cordova A-7 and A-8
      - Cordova B-4
      - Demarcation Point D-2
      - Dixon Entrance C-1, C-3, D-2, and D-5
      - Flaxman Island A-3
      - Hooper Bay D-3
      - Iliamna B-2
      - Kenai B-6
      - Ketchikan B-1
      - Kodiak A-4
      - Kotzebue C-1
      - Mount Fairweather B-4
      - Mount Katmai A-3, and B-1
      - Noatak C-5
      - Norton Bay B-5
      - Nunivak Island C-1
      - Nushagak Bay C-1, C-4 and C-5
      - Point Hope B-3, and D-2
      - Port Moller D-3, and D-4
      - Saint Michael A-4, and A-5
      - Sitka A-6, and C-7
      - Skagway B-8
      - Stepovak Bay A-5, and D-4
      - Sumdum B-2
      - Sutwik Island A-3, and C-4
      - Taku River B-5, and C-6
      - Trinity Islands C-1
      - Ugashik A-2
      - Unimak B-2

6. Removed some duplicate cells (same name, so not clear which will be used
   to set the footprint)
   - Historic ITM
     - Smaller False Pass D-0. (need the larger extents)
     - Smaller Mount Katmai B-1. (need the larger extents)
     - Sutwik Island A-3 has two versions with the same extents, I edited one
       to include some overflow, so I deleted the other to avoid confusion.

7. Some of the historic maps are not in NAD27, so the NAD27 clipping footprints
   do not work correctly. A small unix shell script (`Tools\find_no27.sh`) was
   used to run `gdalinfo` on any file with a date in the file name newer than
   1980. It printed the datum for any of those files without a 1927 datum.
   For these files, the cell name was modified to have 'WGS84' appended, and
   footprints from the original NAD83 data were copied into a new NAD83
   feature class `Cell_Polygons_Historic_WGS84` in `NPS_Processing_Data.gdb`.
   The cell names were modified to have WGS84 appended.  It is important to
   distinguish by cell name, because the import footprint tool applies to all
   rasters (there is no way to only import a subset)  

    - Historic_QQ
      - AK_Saint George Island East_353770_2001_25000_geo.tif - DATUM: "World Geodetic System 1984"
      - AK_Saint George Island West_353771_2001_25000_geo.tif - DATUM: "World Geodetic System 1984"
      - AK_Saint Paul Island East_353772_2001_25000_geo.tif - DATUM: "World Geodetic System 1984"
      - AK_Saint Paul Island West_353773_2001_25000_geo.tif - DATUM: "World Geodetic System 1984"

    - Historic_QM
      - AK_Port Moller_361322_1988_250000_geo.tif - DATUM: "World Geodetic System 1984"

    - Historic_ITM
      - Anchorage/AK_Anchorage A-7_361733_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage A-8_361734_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage B-4_361735_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage B-5_361736_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage B-6_361730_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage B-7_361731_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage B-8_353982_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage C-2_353988_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage C-3_353992_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage C-4_353996_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage C-5_354002_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage C-6_354009_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage C-7_354014_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage C-8_354018_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-1_354025_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-2_354032_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-3_354037_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-4_354044_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-5_354050_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-6_354057_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-7_354063_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Anchorage/AK_Anchorage D-8_354069_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Atlin/AK_Atlin A-7_463497_2004_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Atlin/AK_Atlin A-8_463498_2004_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Kenai/AK_Kenai C-1_356609_1992_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Kenai/AK_Kenai C-2_356614_1992_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Kenai/AK_Kenai C-3_356621_1992_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy A-4_357268_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy A-6_357275_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy B-4_357290_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy B-6_357298_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy B-7_357303_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy B-8_357306_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy C-4_357316_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy C-5_357320_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy C-6_357325_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy C-7_357329_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - McCarthy/AK_McCarthy C-8_357333_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Skagway/AK_Skagway A-1_464119_2004_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Skagway/AK_Skagway A-2_464121_2004_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Skagway/AK_Skagway B-1_464122_2004_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Skagway/AK_Skagway C-1_464124_2004_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Talkeetna/AK_Talkeetna A-1_359509_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Talkeetna/AK_Talkeetna A-2_359514_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Talkeetna/AK_Talkeetna B-1_359530_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Talkeetna/AK_Talkeetna B-2_359536_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Tyonek/AK_Tyonek C-1_360033_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Tyonek/AK_Tyonek C-2_360041_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Tyonek/AK_Tyonek C-3_360044_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Tyonek/AK_Tyonek D-1_360057_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Tyonek/AK_Tyonek D-2_360064_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Tyonek/AK_Tyonek D-4_360072_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez A-1_360273_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez A-2_360276_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez A-3_360279_1994_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez B-1_360305_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez B-3_360312_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez B-5_360321_1995_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez B-6_360325_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez C-2_360339_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez C-3_360343_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez C-4_360349_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez C-5_360354_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez C-6_360359_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez C-7_360364_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez C-8_360368_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-1_360372_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-2_360376_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-3_360382_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-4_360383_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-5_360390_1996_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-6_360395_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-7_360399_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
      - Valdez/AK_Valdez D-8_360404_1993_63360_geo.tif - DATUM: "World Geodetic System 1984"
