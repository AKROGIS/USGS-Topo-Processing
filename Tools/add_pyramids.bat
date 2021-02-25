@ECHO OFF
SETLOCAL ENABLEEXTENSIONS
SETLOCAL ENABLEDELAYEDEXPANSION

REM This script adds overviews to all the *.tif files below the current folder
REM to use GDAL commands you must first run SDKShell.bat from the GDAL folder

FOR /R %%f in  (*.tif) DO (
    SET "src=%%f"
    gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL -r average "!src!" 3 9 27 81
)