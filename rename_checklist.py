#this code changes the file names from geonames id to country name
#it creates a directory for each country and places the tsv file in that directory
#the country name is all lower case with underscores for spaces
#be sure to change the file paths for your local machine

import os
import pickle
import re
import shutil

f = open('country_dict.p', 'rb')

country_ids = pickle.load(f)

for filename in os.listdir('/Volumes/PCCOMP/effechecka_country_results/checklist/'): #this path needs to point to the unzipped effechecka output
	if not filename.startswith('.'): #this ignores hidden files. I'm not sure why they are there
		name = re.sub('.tsv', '', filename)
		country = country_ids[name]
		if not os.path.exists('/Volumes/PCCOMP/effechecka_country_results/' + country + '/'):
			os.makedirs('/Volumes/PCCOMP/effechecka_country_results/' + country + '/')
		shutil.copy('/Volumes/PCCOMP/effechecka_country_results/checklist/' + filename, '/Volumes/PCCOMP/effechecka_country_results/' + country + '/' + country)
	else:
		os.remove(filename) #this removes the hidden files