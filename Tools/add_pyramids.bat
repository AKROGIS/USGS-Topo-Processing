@ECHO OFF
SETLOCAL ENABLEEXTENSIONS
SETLOCAL ENABLEDELAYEDEXPANSION

REM to use GDAL commands you must first run the command C:\users\resarwas\gdal\SDKShell.bat

FOR /R %%f in  (*.tif) DO (
    SET "src=%%f"
    gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL -r average "!src!" 3 9 27 81
)