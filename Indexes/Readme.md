# Indexes

**NOTE** This section needs to be updated.

* `MAPINDICES_Alaska_State_GDB.gdb` - A file geodatabase downloaded from the
  National Map, that has the polygon extents (footprint) for data portion of
  each map (i.e. it excludes the marginalia). See the metadata for the date
  of the data.  Typically the `cell name` matches the root filename of the maps.
  These indexes can be used to provide clipping footprints for each map tile
  in the mosaics  The indexes are in the NAD83 datum which causes some problem
  with the historic map (in NAD27).  See the section on _Processing Notes_ for
  details.  In addition, the polygon extents are "nominal", i.e. they do not
  include data that "bleeds into the marginalia" on some maps.
* `MAPINDICES_Alaska_State_GDB.xml` - FGDC Metadata for the database.
* `NPS_Processing_Data.gdb` - Created to hold the NAD27 version of the
  Footprints.  See the section on _Historic Footprints_ below.
* `{itm|qq|qm}_data.csv` - files with filename attributes separated into columns
  as well as manually collected data (print date, etc) to help categorize and
  select the best available among multiple versions of a map.
* `nationalmap_search_results*.csv` - search results from the national map
  that provide the source URL and additional metadata for each downloaded file.
