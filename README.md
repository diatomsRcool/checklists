# checklists

This repository contains code for making checklists for countries using the effechecka API. There are two ways to run this code. You can make one or two lists using the jupyter notebook or you can bulk submit using Jenkins. The jupyter notebook is good for seeing more of what is going on, but is a slower, more manual process. The code works by submitting polygons to effechecka which then assembles deduplicated lists of all the taxa with occurrence data within the polygon. The polygons used in this code are from GeoNames.

## Getting the Polygons

GeoNames has an API that allows users to look up a country ID and get the geolocated polygon. Some of these polygons were too long, so the resolution of the national borders had to be reduced. The polygons were translated into wkt strings for submission to effechecka.

## Getting the lists

The effechecka API was used in two steps. First, the query has to be submitted, then the results downloaded. Since these are very large lists, they can take some time between the initial query and completion of the list. The first time a query is submitted, effechecka starts compiling the list. The second time it is submitted, the results are downloaded, if they are ready. If they are not ready, you will have to submit the query again later. The Jenkins job will automatically do this for you, but not the jupyter notebook. The code for the Jenkins job is in the checklists_script_gen.sh and .

## Making the TraitBank files

Effechecka gives lists back as tsv files. These need to be translated into DwC format for upload into TraitBank. This requires two pieces of code that process each list. The first block of code makes the dictionaries needed to keep track of all the taxon ids and parent ids. The second block of code generates the TraitBank files. These files are compressed and uploaded into EOL opendata for eventual upload into TraitBank. Each country will have its own TraitBank DwC-A.
