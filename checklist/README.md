# Checklist

This directory contains the code that is run as a Jenkins job at archive.guoda.bio

The wkt_string.tsv file contains polygons for all the countries formatted as wkt_strings. The countries are identified using their geonames ID. The polygons were obtained from GeoNames. Some of them had to be shortened to accommodate limits in the length of the API call. Polygons were shortened by reducing resolution and/or using "bounding polygons", in the case of island groups.

The checklist_script_gen.sh file generates the API calls and reports the status of each list. When each query in the list returns a 200 html status, the checklist_download.sh script is run and downloads all the results into the checklist directory.

## Notes
I was never able to get Antarctica to work. Effechecka does not support wrapping polygons around the poles or over the international dateline.
