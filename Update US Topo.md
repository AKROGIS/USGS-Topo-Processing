# US Topo Update

* Get the last update from the end of the file
  `X:\Extras\AKR\Statewide\Charts\USGS_Topo\Indexes\nationalmap_search_results_pdf_YYYYMMDD.csv`
  with the most recent date
* Open https://viewer.nationalmap.gov/basic/
  - Click `Datasets` tab
  - Select `US Topo` under the `Maps` section
  - Click on `Advanced Search Options`
    - Select `Date Range`
    - For Data Type, select `Last Update` in the picklist
    - Start Date = last update date from above
    - End Date = today
  - Zoom/Pan map (and change browser aspect ration) so that **ALL** of Alaska
    is visible, and **NO** other states are visible.
  - CLick the big `Find Products` button.
  - Click the `Save as CSV` Button
    - Save as lastupdateYYYYMMDD.csv
 - click `Return to Search` button
   - Change Data Type, select `Date Created` in the picklist
  - Click the big `Find Products` button.
  - Click the `Save as CSV` Button
    - Save as createdYYYYMMDD.csv
* compare/merge two download files to make a single unique list
  - Large files are easiest to check by importing to SQL server
  - Smaller files can be opened in Excel and compared.
  - A cheat is to just select hte file with more records
  - or Open the two files and compare with windiff
  - or make the uget list for both files and compare with windiff
* Make Uget list
  - Copy `X:\Extras\AKR\Statewide\Charts\USGS_Topo\Tools\make_uget_list.py` to a working directory
  - Edit `make_uget_list.py` line 10 to use the input path from above
  - Run `make_uget_list.py` with Python2.7
    - If there is an error,  make sure there is no empty line at the end of the file.
  - Run it again with other download list
  - Change the file names to .csv
  - open in Excel, sort, and delete duplicates then save
  - rename to *.txt

* Download larger of the two uget lists
* Run merge_unique_uget.py to get a list of files in 2nd, but not first uget list
* Downlod the third uget list
* Compare the downloaded files with the X drive files to find which are new/dups/updates
* run `remove_dups.py` to remove the dups.
* put the downloaded pdfs in a `Current_GeoPDF` folder
* create a `Curent_GeoTIFF` folder adjacent to the `Current_GeoPDF`
* Run `arrange_topos.py`
* run `create_gdal_batchfile.py`
* break into 8 equal chunks
* open a new comand prompt
  - run c:\resarwas\gdal3\sdkShell.bat
  - cd to folder with batch file
  - run batch file
* repeat for all 8 batch files
  - each batch file will take about 5-15 minutes per line. if there are only a few files to process, then fewer batch files may be better.
* when done, close all but one command window
* In the remainng command window run `add_pyramids.bat`
   - takes about 5 seconds per file to finish.