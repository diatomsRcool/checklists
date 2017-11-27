import pickle
import re

in_file = open('country_list_1.txt', 'r')
p_file = open('wkt_string.tsv', 'r')

country_dict = {}
id_dict = {}
p_dict = {}

for line in in_file:
	line = line.strip('\n')
	row = line.split('\t')
	id = row[2]
	country = row[0]
	country_ = re.sub('\s', '_', country)
	country_ = country_.lower()
	country_dict[id] = country_
pickle.dump(country_dict, open('country_dict.p', 'wb'))

in_file.seek(0)

for line in in_file:
	line = line.strip('\n')
	row = line.split('\t')
	id = row[2]
	country = row[0]
	print(country)
	id_dict[country] = id
pickle.dump(id_dict, open('id_dict.p', 'wb'))

for line in p_file:
	line = line.strip('\n')
	row = line.split('\t')
	id = row[0]
	polygon = row[1]
	p_dict[id] = polygon
pickle.dump(p_dict, open('polygon_dict.p', 'wb'))
	
