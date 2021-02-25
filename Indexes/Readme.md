# Indexes

## `MAPINDICES_Alaska_State_GDB.gdb`

A file geodatabase downloaded from the
National Map, that has the polygon extents (footprint) for data portion of
each map (i.e. it excludes the marginalia). See the metadata for the date
of the data.  Typically the `cell name` matches the root filename of the maps.
These indexes can be used to provide clipping footprints for each map tile
in the mosaics  The indexes are in the NAD83 datum which causes some problem
with the historic maps(in NAD27).  See the
[Initial Process Instructions](../Initial_Process_Instructions.md) for
how this was resolved.  In addition, the polygon extents are "nominal", i.e.
they do not include data that "bleeds into the marginalia" on some maps.

## `MAPINDICES_Alaska_State_GDB.xml`

FGDC Metadata for the USGS index database.

## `NPS_Processing_Data.gdb`

Created to hold the NAD27 version of the footprints.  See the section on
_Historic Footprints_ in the
[Initial Process Instructions](../Initial_Process_Instructions.md).
These were the footprints used to create the historic mosaics, and were
altered as needed to include any map that bled into the marginalia.

## `all_metadata_{itm|qq|qm|topo}.csv`

Metadata for each file in the category in the name.  These files are created
with the [make_alaska_lists script](../Tools/make_alaska_lists.py) from the
downloaded USGS database.  The data in these files has been added to the
respective raster mosaic datasets in order to describe, sort and filter the
tiles in each mosaic. The veracity of some attributes is suspect, for example,
I found 1:250k tiles that were shaded reliefs, but not described as such.

## `last_processing_date.txt`

The date of the last download from USGS and the creation of the download and
metadata files.

## `new_downloads_{itm|qq|qm|topo}.csv`

This file describes the files in the named category that were downloaded
during the last refresh.  The commit history will show the lists of files
downloaded in the past.

## `{itm|qq|qm}_data.csv`

Files with filename attributes separated into columns
as well as manually collected data (print date, etc) to help categorize and
select the best available among multiple versions of a map.
