import urllib.request
from bs4 import BeautifulSoup
import pickle
import json
import re

in_file = open('/Users/annethessen/checklists/country_list_1.txt', 'r')

countries = []

for line in in_file:
	line = line.strip('\n')
	row = line.split('\t')
	m = []
	name = row[0]
	#print(name)
	if name == 'Georgia':
		t = name + '_(country)'
	t = re.sub(' ', '_', name)
	id = row[2]
	#print(id)
	m.append(t)
	m.append(id)
	#print(m)
	countries.append(m)
#print(countries)

out_file = open('geography_data.txt', 'w')

out_file.write('country	geonames_id	area_km2	percent_water	population_density	gdp_nominal	gdp_ppp	gini	hdi\n')

for y in countries:
	country = y[0]
	id = y[1]
	if country == 'Tibet':
		continue
	url = 'https://en.wikipedia.org/api/rest_v1/page/html/' + country
	print(url)
	results = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(results, 'html.parser')
	infobox = json.loads(soup.table['data-mw'])
	test = infobox['parts'][0]['template']['target']['wt']
	if test == 'refimprove' or test == 'Refimprove' or test == 'refimprove\n' or test == 'Update':
		area = ''
		p_water = ''
		pop_den = ''
		gdp = ''
		gini = ''
		hdi = ''
	else:
		data = infobox['parts'][0]['template']['params']
		if 'area_km2' in data:
			area = data['area_km2']['wt']
		elif 'area km2' in data:
			area = data['area km2']['wt']
		else:
			print('check area')
		#print(area)
		if 'percent_water' in data:
			p_water = re.sub(' <!--CIA World Factbook-->', '', data['percent_water']['wt'])
		else:
			p_water = ''
		#print(p_water)
		if 'population_density_km2' in data:
			pop_den = data['population_density_km2']['wt']
		elif 'density km2' in data:
			pop_den = data['density km2']['wt']
		else:
			print('check pop den')
		#print(pop_den)
		if 'GDP_nominal_per_capita' in data:
			gdp_n = re.sub('<ref name=imf2/>|<ref name=IMF />|<ref name="IMF GDP" />|<ref name=imf/>|<ref name="imf" />|<ref name="imf2" />|<ref name="IMF"/>|<ref name=imf2 />|<ref name=WEO2017/>|<ref name=GDP />|<ref name="imf2"/>|<ref name="IMF GDP"/>|<ref name=IMF/>|<ref name="imf"/>|<ref name="imf.org"/>', '', data['GDP_nominal_per_capita']['wt'])
		else:
			gdp_n = ''
		if 'GDP_PPP_per_capita' in data:
			gdp_p = re.sub('<ref name=imf2/>|<ref name=IMF />|<ref name="IMF GDP" />|<ref name=imf/>|<ref name="imf" />|<ref name="imf2" />|<ref name="IMF"/>|<ref name=imf2 />|<ref name=WEO2017/>|<ref name=GDP />|<ref name="imf2"/>|<ref name="IMF GDP"/>|<ref name=IMF/>|<ref name="imf"/>|<ref name="imf.org"/>', '', data['GDP_PPP_per_capita']['wt'])
		else:
			gdp_p = ''
		#print(gdp)
		if 'Gini' in data:
			gini = re.sub(' <!--number only-->|<!-- Number only. -->|<!--number only-->| <!-- number only -->|<!-- number only -->', '', data['Gini']['wt'])
		else:
			gini = ''
		#print(gini)
		if 'HDI' in data:
			hdi = re.sub(' <!--number only-->| <!-- Number only. -->|<!--number only-->| <!-- number only -->|<!-- number only -->', '', data['HDI']['wt'])
		else:
			hdi = ''
	out_file.write(country + '\t' + str(id) + '\t' + area + '\t' + p_water + '\t' + pop_den + '\t' + gdp_n + '\t' + gdp_p + '\t' + gini + '\t' + hdi + '\n')	
out_file.close()