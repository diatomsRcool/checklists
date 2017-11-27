import os
import pickle
import re

f = open('/Users/annethessen/checklists/country_dict.p', 'rb')

country_ids = pickle.load(f)

for filename in os.listdir("."):
	if filename == '2461445.tsv':
		continue
	else:
		name = re.sub('.tsv', '', filename)
		os.rename(filename, country_ids[name])
"""
for filename in os.listdir("."):
	os.rename(filename, filename + '.tsv')
"""