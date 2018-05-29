# checklists

This repository contains code for making checklists for countries using the effechecka API. There are two ways to run this code. You can make one or two lists using the jupyter notebook or you can bulk submit using Jenkins. The jupyter notebook is good for seeing more of what is going on, but is a slower, more manual process. The code works by submitting polygons to effechecka which then assembles deduplicated lists of all the taxa with occurrence data within the polygon. The polygons used in this code are from GeoNames.

## Getting the Polygons

GeoNames has an API that allows users to look up a country ID and get the geolocated polygon. Some of these polygons were too long, so the resolution of the national borders had to be reduced. The polygons were translated into wkt strings for submission to effechecka.

## Getting the lists

The effechecka API was used in two steps. First, the query has to be submitted, then the results downloaded. Since these are very large lists, they can take some time between the initial query and completion of the list. The first time a query is submitted, effechecka starts compiling the list. The second time it is submitted, the results are downloaded, if they are ready. If they are not ready, you will have to submit the query again later. The Jenkins job will automatically do this for you, but not the jupyter notebook. The code for the Jenkins job is in checklists_script_gen.sh.

## Making the TraitBank files

Effechecka gives lists back as tsv files. These files are downloaded into a checklists directory with the id # used to tag the wkt string as the file name. When all the checklists are downloaded, the directory is compressed and then is ready for download onto a local machine. These files are much too large for GitHub, so they need to be downloaded locally for further processing.

These need to be translated into DwC format for upload into TraitBank. This requires two pieces of code that process each list. The first block of code makes the dictionaries needed to keep track of all the taxon ids and parent ids. The second block of code generates the TraitBank files. These files are compressed and uploaded into EOL opendata for eventual upload into TraitBank. Each country will have its own TraitBank DwC-A.

## File Descriptions

Build_Taxon.ipynb - Jupyter notebook that takes a tsv checklist and creates the dictionaries needed to manage the taxon and parent ids during the process of building the TraitBank Darwin Core Archives.

Make_TB_file.ipynb - Jupyter notebook that reads the tsv checklist and creates the Darwin Core archive needed for upload into TraitBank. The taxon and parent IDs are managed via dictionaries that were made using Build_Taxon.ipynb

bird_data.txt - a list of all countries, their geonames ID, the number of bird species, and the number of bird observations. this is the output from get_birds.py

build_continent_dict.py - This code creates a look up dictionary from a list of contries and their continents. Country is the key and continent is the value. This code created continent_dict.p

checklist_script_gen.sh - A bash script for creating the effechecka queries from a list of wkt strings (wkt_string.tsv). It also creates two other scripting files, checklist_status.sh and checklist_download.sh. These are the scripts that run in Jenkins. Every time this GitHub repository is updated, the Jenkins job is triggered. So, if the wkt_string.tsv file is updated, the scripts get run automatically.

continent_dict.p - a dictionary for looking up a country's continent. Country name with underscore instead of spaces is the key and the two-letter continent abbreviation is the value. Use the Python pickle module to load the dictionary.

country_dict.p - a dictionary for looking up country by geonames ID. Geonames ID is the key and country is the value. Use the Python pickle module to load the dictionary.

country_list_1.txt - tab-delimited list of the countries, their two letter abbreviations, and their geonames ID. One country per row. A few more political areas have been added, such as Tibet and Puerto Rico.

get_birds.py - This code goes through all the checklists and finds all the birds. It outputs a row with the country name, country Geonames ID, number of bird species, and number of bird observations.

get_effechecka_data.ipynb - This is the jupyter notebook that can be used to submit one or two countries to the effechecka API to generate the checklist.

id_dict.p - a dictionary for looking up a country's geonames ID. Country is the key and geonames ID is the value. Use the Python pickle module to load the dictionary.

low_res_countries.json - This json file has the polygons for each country connected to their geonames ID. This file was created by reduce_polygon.ipynb

make_continent_list.py - This code generated the checklists for the continents.

make_country_dict.py - This code created country_dict.p, id_dict.p, and polygon_dict.p

make_taxon_records_data.py - This code created a file called taxon_data.txt that gives the number of observations of each family in each country. This was part of my exploration of checklists and geographic data.

make_wkstring.py - This code makes wkt strings for every polygon in low_res_countries.json. These are the wkt strings used by checklists_script_gen.sh

parent_dict.p - This dictionary is for looking up a parent for any taxon. The taxon is the key and its parent is the value. It is created by make_taxon_dict.py and Build_Taxon.ipynb

polygon_dict.p - This dictionary allows looking up a polygon by the corresponding country's geonames id. It was created by make_country_dict.py

reduce_polygon.ipynb - This code was used to reduce the length of the polygons that were too large to fit in the API query

taxon_data.txt - The results of make_taxon_records_data.py. It is a list of all families from each country and their number of observations.

taxon_id.p - This dictionary is for looking up the taxon id for any taxon. The taxon is the key and its id is the value. It is created by make_taxon_dict.py and Build_Taxon.ipynb. The identifier is question is local and only valid within the Darwin Core Archive.

tb_measurement.txt - One of the data files for the TraitBank Darwin Core Archive. Created by make_tb_file.py or Make_TB_file.ipynb

tb_occurrence.txt - One of the data files for the TraitBank Darwin Core Archive. Created by make_tb_file.py or Make_TB_file.ipynb

tb_taxon.txt - One of the data files for the TraitBank Darwin Core Archive. Created by make_tb_file.py or Make_TB_file.ipynb

test_country.txt - I list of only a few countries used for testing purposes.

wkt_string.tsv - A list with one wkt string for each country and its geonames ID. This file is used by checklists_script_gen.sh to formulate the effechecka queries
