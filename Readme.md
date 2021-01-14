# USGS Topographic Maps

This folder contains Topographic Maps from USGS and related files.
These data are primarily snapshots of files available from the
[National Map](https://viewer.nationalmap.gov). See
[Initial_Process_Instruction](./Initial_Process_Instructions.md) for details
on how these files were initially collected and processed. See
[Update_Instructions](Update_Instructions.md) for how they are maintained.

Created by: Regan Sarwas, Alaska NPS GIS Team.
Last Edited: 2021-01-13.

*The master copy of the documents and scripts in this folder is at
<https://github.com/AKROGIS/USGS-Topo-Processing>.  The Github repository
does not contain the PDF and GeoTIFF files nor the file geodatabases.*

**NOTE:** Most historic maps are in NAD27, while the current maps and the
Indexes are in NAD83.

## Current_GeoPDF

These files are the modern 1:25k PDF topographic maps of Alaska downloaded from
the national map, and then organized into sub folders.  There may be multiple
versions of a map (the published date is encoded in the file name).
The base of the file name matches the names in the `cell_name` column
of the geodatabase in the `Indexes` folder.  The indexes provide a clipping
polygon for each map. The filename (cell_name) may not match the historic
names, for example Mt McKinley was rename Denali in August of 2015. Additional
metadata for each file is in the list of the national map search results in the
`Indexes` folder.

## Current_GeoTIFF

The files in this folder are geoTIFF files created with [GDAL](https://gdal.org)
from the contents of the `Current_GeoPDF` folder. The geoTIFFs are RGB images at
600dpi. They do not include the imagery, PLSS, other grids, or marginalia
available in the PDF version.  This folder only includes the most recent PDF
files. They are created for use in a statewide mosaic. The organization mimics
the organization in the `Current_GeoPDF`. As the contents of the `Current_GeoPDF`
folder are updated, this folder should also be updated.  To allow the mosaic
to stay current without re-adding source rasters, the geoTIFFs have dropped
the date from the filename.  Each file should reflect the most current data
for that tile.

## Historical_ITM

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

## Historical_QM

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
in the `Indexes` folder.

## Historical_QQ

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
search results in the `Indexes` folder.

## Indexes

A folder with a file geodatabase with footprints for each map, and lists of maps
with metadata (some from USGS, and some from me). See the Readme in this folder
for additional details.

## Tools

Scripts for updating the contents of the above folders and other derived
products with updated data from the USGS.  See the Readme in this folder for
additional details.
