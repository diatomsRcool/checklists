#this code changes the file names from geonames id to country name
#it creates a directory for each country and places the tsv file in that directory
#the country name is all lower case with underscores for spaces
#be sure to change the file paths for your local machine

import os
import pickle
import re

f = open('country_dict.p', 'rb')

country_ids = pickle.load(f)

for filename in os.listdir('/Volumes/PCCOMP/checklist'): #this path needs to point to the unzipped effechecka output
	name = re.sub('.tsv', '', filename)
	country = country_ids[name]
	if not os.path.exists('/Volumes/PCCOMP/effechecka_country_results/' + country + '/'):
		os.makedirs('/Volumes/PCCOMP/effechecka_country_results/' + country + '/')
	os.rename(filename, '/Volumes/PCCOMP/effechecka_country_results/' + country + '/' + country)
