import pickle
import re

in_file = open('country_list_1.txt', 'r')
out_file = open('oceania.txt', 'w')
f = open('continent_dict.p', 'rb')

out_file.write('taxonName	taxonPath	recordCount\n')

continents = pickle.load(f)

continent = 'OC'

checklist = []

for line in in_file:
	line = line.strip('\n')
	row = line.split('\t')
	country = row[0]
	country = re.sub('\s', '_', country)
	country = country.lower()
	print(country)
	if continents[country] == continent:
		list_file = open('/Users/annethessen/effechecka_country_results/' + country + '/' + country + '.tsv', 'r')
		next(list_file)
		for line_ in list_file:
			line_ = line_.strip('\n')
			row_ = line_.split('\t')
			classification = row_[1].split('|')
			#print(len(classification))
			if len(classification) < 7:
				continue
			else:
				genus = classification[5]
				species = classification[6]
				taxon = genus + ' ' + species
				if taxon in checklist:
					continue
				else:
					checklist.append(taxon)
					out_file.write(line_ + '\n')