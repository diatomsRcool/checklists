#This code uses the GeoNames API to look up geonames ids for countries by the country's 
#name.

import urllib
import json

in_file = open('country_list.txt', 'r')
out_file = open('country_list_1.txt', 'w')


for line in in_file:
	line = line.strip()
	row = line.split('\t')
	country = row[1]
	print country
	url = 'http://api.geonames.org/countryInfoJSON?country=' + country + '&username=annethessen'
	results = urllib.urlopen(url).read()
	#print results
	data = json.loads(results)
	geonameid = data['geonames'][0]['geonameId']
	out_file.write(line + '\t' + str(geonameid) + '\n')