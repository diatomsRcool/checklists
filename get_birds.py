#This code iterates over all the country checklists and collects the bird data. The output is a list of all the
#countries with the number of bird taxa and number of bird observations.

import urllib.request
from bs4 import BeautifulSoup
import pickle
import json
import re

in_file = open('/Users/annethessen/checklists/country_list_1.txt', 'r') #list of countries and their geonames ID

#This function normalizes the length of the hierarchy returned by effechecka. Sometimes taxa come back
#with different numbers of parents
def norm_len(hi_class):
    #print(len(hi_class))
    skip = False
    if len(hi_class) == 1:
        skip = True
    elif len(hi_class) < 3:
        hi_class.insert(3, '')
        hi_class.insert(4, '')
        hi_class.insert(5, '')
        hi_class.insert(6, '')
        hi_class.insert(7, '')
    elif len(hi_class) < 4:
        hi_class.insert(4, '')
        hi_class.insert(5, '')
        hi_class.insert(6, '')
        hi_class.insert(7, '')        
    elif len(hi_class) < 6:
        hi_class.insert(5, '')
        hi_class.insert(6, '')
        hi_class.insert(7, '')
    elif len(hi_class) < 7:
        hi_class.insert(3, '')
        name = hi_class[5].split(' ')
        if len(name) < 2:
            skip = True
        else:
            print(hi_class)
            print(name)
            genus = name[0]
            spec = name[1]
            hi_class.insert(5, genus)
            hi_class.insert(6, spec)
    elif len(hi_class) < 8:
        name = hi_class[6].split(' ')
        if len(name) < 2:
            skip = True
        else:
            spec = name[1]
            hi_class.insert(6, spec)
    else:
        pass
    return hi_class, skip

countries = []

#This creates a list of countries with the spaces substituted with underscores and with their ids
for line in in_file:
	line = line.strip('\n')
	row = line.split('\t')
	m = []
	name = row[0]
	#print(name)
	t = re.sub(' ', '_', name)
	id = row[2]
	#print(id)
	m.append(t)
	m.append(id)
	#print(m)
	countries.append(m)
#print(countries)

out_file = open('bird_data.txt', 'w') #resulting data file

out_file.write('country	geonames_id	#bird_species	#_bird_obs\n')

#using the list of countries made above, we will find the corresponding data directory and iterate over the
#checklist that was returned from effechecka. All the species that are in Aves will be captured and used in
#calculations
for y in countries:
	country = y[0]
	print(country)
	id = y[1]
	if country == 'Tibet' or country == 'Hong_Kong' or country == 'Antarctica':
		continue
	data = open('/Users/annethessen/effechecka_country_results/' + country + '/' + country + '.tsv', 'r')
	taxa = []
	count = 0
	next(data)
	for line in data:
		line = line.strip('\n')
		row = line.split('\t')
		classification = row[1].split('|')
		for i,j in enumerate(classification): #this for loop removes any incertae sedis. We don't want that as a taxon.
			if j == 'incertae sedis':
				classification[i] = ''
		classification, r = norm_len(classification) #using the function to normalize lengths
		if r == True:
			continue
		else:
			kingdom = classification[0].title()
			phylum = classification[1].title()
			class_ = classification[2].title()
			order = classification[3].title()
			family = classification[4].title()
			genus = classification[5].title()
			species = classification[6]
			if species == '' or genus == '': #if its not identified to species, then we don't want it
				continue
			else:
				#print(order)
				if class_ == 'Aves':
					records = int(row[2])
					taxon = genus + ' ' + species
					if taxon in taxa:
						continue
					else:
						taxa.append(taxon)
						count = count + records
				else:
					continue
	out_file.write(country + '\t' + str(id) + '\t' + str(len(taxa)) + '\t' + str(count) + '\n')	
out_file.close()
