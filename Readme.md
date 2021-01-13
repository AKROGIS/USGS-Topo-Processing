USGS Topographic Maps
=====================

This folder contains Topographic Maps from USGS and related data.

Created by: Regan Sarwas, Alaska NPS GIS Team
Last Edited: 2020-01-06

These data are primarily snapshots of files available
from the [National Map](https://viewer.nationalmap.gov).

**The historic maps are in NAD27, while the current maps and the
Indexes are in NAD83**

Current_GeoPDF
--------------
These files are the modern 1:25k topo maps of Alaska downloaded from the
national map, and then organized into sub folders.  There may be multiple
versions of a map (the published date is encoded in the file name).
The base of the file name matches the names in the `cell_name` column
of the geodatabase in the `Indexes` folder.  The indexes provide a clipping
polygon for each map. The filename (cell_name) may not match the historic
names, for example Mt McKinley was rename Denali in August of 2015. Additional
metadata for each file is in the list of the national map search results in the
`Indexes` folder. See the _Processing Notes_ section below for details on how
these files were collected and maintained.

Current_GeoTIFF
---------------
The files in this folder are geoTIFF files created with GDAL from the contents
of the `Current_GeoPDF` folder. The geoTIFFs are RGB images at 600dpi.
They do not include the imagery, PLSS, other grids, or marginalia available
in the PDF version.  This folder only includes the most recent PDF files.
They are created for use in a statewide mosaic. The organization mimics
the organization in the Current_GeoPDF. As the contents of the Current_GeoPDF
folder are updated, this folder should also be updated.  To allow the mosaic
to stay current without re-adding source rasters, the geoTIFFs have dropped
the date from the filename.  Each file should reflect the most current data
for that tile.  See the Processing Notes section below for details on how
these files were created and maintained.

Historical_ITM
--------------
This folder contains historical quadrangle (quad) maps with an extents of
15 x 15 minutes or 16th of a 1 x 1 degree cell. These maps are also know as
inch to mile (itm), because most are at a scale of 1:63360 or 1 inch = 1 mile.
These maps are scanned (300dpi) geoTIFF files downloaded from The National Map.
These maps are organized into folders based on the root name.  There are
multiple versions of most maps.  These may vary by revision and/or printing
date, but some only differ based on the color gamut of the printed product.
The file name only includes the original publication date, so additional data
needed to differentiate and categorize maps with the same extents is maintained
in the file called `itm_data.csv` in the `Indexes` folder. Additional metadata
for each file is in the national map search results in the `Indexes` folder.
See the _Processing Notes_ section below for details on how these files were
collected and maintained.

Historical_QM
-------------
This folder contains historical quadrangle (quad) maps with an extents of
of 1x1, 1x2, 1x3, or 1x4 degrees depending on latitude (typical 1x2 degrees).
These maps are also know as quarter million quads (qm) because all are at a
scale of 1:250,000. These maps are scanned (300dpi) geoTIFF files downloaded
from The National Map. There are multiple versions of each maps.  Some versions
include shaded relief, bathymetric data, or military grids. They may also vary
by revision and/or printing date, but some only differ based on the color gamut
of the printed product. The file name only includes the original publication
date, so additional data needed to differentiate and categorize maps with the
same extents is maintained in the file called `qm_data.csv` in the `Indexes`
folder. Additional metadata for each file is in the national map search results
in the `Indexes` folder. See the _Processing Notes_ section below for details
on how these files were collected and maintained.

Historical_QQ
-------------
This folder contains historical quadrangle (quad) maps with an extents of
of 7.5 x 7.5 minutes, or one quarter of a standard (itm) quad map, hence the
nickname quarter-quad (qq). These maps are scanned (300dpi) geoTIFF files
downloaded from The National Map. There are multiple versions of most maps.
Some of the maps include a photo background, while others do not. Maps may
also vary by revision and/or printing date, but some only differ based on the
color gamut of the printed product. The file name only includes the original
publication date, so additional data needed to differentiate and categorize
maps with the same extents is maintained in the file called `qq_data.csv` in
the `Indexes` folder. Additional metadata for each file is in the national map
search results in the `Indexes` folder. See the _Processing Notes_ section
below for details on how these files were collected and maintained.

Indexes
-------
* MAPINDICES_Alaska_State_GDB.gdb - A file geodatabase downloaded from the
  National Map, that has the polygon extents (footprint) for data portion of
  each map (i.e. it excludes the marginalia). See the metadata for the date
  of the data.  Typically the `cell name` matches the root filename of the maps.
  These indexes can be used to provide clipping footprints for each map tile
  in the mosaics  The indexes are in the NAD83 datum which causes some problem
  with the historic map (in NAD27).  See the section on _Processing Notes_ for
  details.  In addition, the polygon extents are "nominal", i.e. they do not
  include data that "bleeds into the marginalia" on some maps.
* MAPINDICES_Alaska_State_GDB.xml - FGDC Metadata for the database.
* NPS_Processing_Data.gdb - Created to hold the NAD27 version of the Footprints.  
  See the section on _Historic Footprints_ below.
* {itm|qq|qm}_data.csv - files with filename attributes separated into columns
  as well as manually collected data (print date, etc) to help categorize and
  select the best available among multiple versions of a map.
* nationalmap_search_results*.csv - search results from the national map
  that provide the source URL and additional metadata for each downloaded file.
