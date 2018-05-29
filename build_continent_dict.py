#This code creates a look up dictionary from a tsv list of countries and their continents.
#The dictionary has country as key and continent as value
#The input file is a list of countries and their continents modified from Wikipedia.

import pickle
import re

in_file = open('continents.tsv', 'r')

continents = {}

for line in in_file:
	line = line.strip('\n')
	row = line.split('\t')
	continent = row[0]
	country = row[4]
	country = re.sub('\s', '_', country)
	country = country.lower()
	#print(country)
	continents[country] = continent
	
pickle.dump(continents, open('continent_dict.p', 'wb'))
	
