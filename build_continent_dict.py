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
	