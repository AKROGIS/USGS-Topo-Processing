 # Bash Shell script
 # finds files with a date in the file name that is 198*, 199*, 200*, or 201*
 # and prints the name and datum if the datum is not NAD 1927
 
 for i in */*_[12][90][8901][0-9]_*.tif; do
  datum=`gdalinfo "$i" | fgrep DATUM`
  if [[ $datum != *"1927"* ]]; then
    echo $i - $datum
  fi
done
