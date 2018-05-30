#This code transforms the effechecka output into TraitBank DwC files
#Be sure that the input and output file paths are set to your local machine

import re
import pickle
import os
from checklist_functions import norm_len,genus_check,check_dict

i = open('polygon_dict.p', 'rb')
polygons = pickle.load(i)

#This file holds the summary statistics for each country. The first list removes any old
#version before starting a new version
#the file paths will be to your local machine
os.remove('/Volumes/PCCOMP/effechecka_country_results/country_stats.txt')
out_file_x = open('/Volumes/PCCOMP/effechecka_country_results/country_stats.txt', 'a')
out_file_x.write('country	geonamesid	taxa	obs\n')

#making a list of countries and their geonames ids to iterate over
country_list = open('country_list_1.txt', 'r') #list of countries and their geonames ID
countries = []
for line in country_list:
	line = line.strip('\n')
	row = line.split('\t')
	m = []
	name = row[0]
	#print(name)
	t = re.sub(' ', '_', name)
	geonames_id = row[2]
	m.append(t.lower())
	m.append(geonames_id)
	#print(m)
	countries.append(m)
country_list.close()

#going through list of countries
for y in countries:
	country = y[0]
	print(country)
	geonames_id = y[1]
	#the in_file is the tsv results from effechecka
	#the file path will be to your local machine
	in_file = open('/Volumes/PCCOMP/effechecka_country_results/' + country + '/' + country + '.tsv', 'r')
	counter = 100000
	kingdoms = []
	phyla = []
	classes = []
	orders = []
	families = []
	genera = []
	species = []
	taxa = []
	parent_dict = {}
	taxon_id = {}
	next(in_file)
	for line in in_file:
		line = line.strip('\n')
		row = line.split('\t')
		taxon_string = row[1].split('|') #the tsv result includes a pipe-delimited higher classification
		for i,j in enumerate(taxon_string): #this for loop removes any incertae sedis. We don't want that as a taxon.
			if j == 'incertae sedis':
				taxon_string[i] = ''
		taxon_string, r = norm_len(taxon_string) #using the function to normalize hierarchy lengths
		if r == True:
			continue
		kingdom = taxon_string[0].title()
		phylum = taxon_string[1].title()
		class_ = taxon_string[2].title()
		order = taxon_string[3].title()
		family = taxon_string[4].title()
		genus = taxon_string[5].title()
		species_e = taxon_string[6]
		genus = genus_check(genus, species_e)
		bl = taxon_string.count('') #not every rank is included, so we need to know how many are missing
		if species_e == '' or genus == '': #if its not identified to species, then we don't want it
			continue
		else:
			taxon = genus + ' ' + species_e
			#this if loop gets rid of some duplication that sneaks into the effechecka
			#results due to slight differences in the name strings
			if taxon in species: 
				pass
			else:
				species.append(taxon) #giving each taxon a local identifier from here to line 118
				taxon_id[taxon] = 'T' + str(counter)
				counter = counter + 1
			if genus in genera:
				pass
			else:
				genera.append(genus)
				taxon_id[genus] = 'T' + str(counter)
				counter = counter + 1
			if family in families or family == '':
				pass
			else:
				families.append(family)
				taxon_id[family] = 'T' + str(counter)
				counter = counter + 1
			if order in orders or order == '':
				pass
			else:
				orders.append(order)
				taxon_id[order] = 'T' + str(counter)
				counter = counter + 1
			if class_ in classes or class_ == '':
				pass
			else:
				classes.append(class_)
				taxon_id[class_] = 'T' + str(counter)
				counter = counter + 1
			if phylum in phyla or phylum == '':
				pass
			else:
				phyla.append(phylum)
				taxon_id[phylum] = 'T' + str(counter)
				counter = counter + 1
			if kingdom in kingdoms or kingdom == '':
				pass
			else:
				kingdoms.append(kingdom)
				taxon_id[kingdom] = 'T' + str(counter)
				counter = counter + 1
			parent_dict[taxon] = taxon_id[genus] #because we ignored everything that was missing a specific epithet or a genus, we don't have to worry about either of them missing
			#from here to line 229 deals with missing ranks. The exact strategy for
			#dealing with the problem depends on how many and which ones are missing. 
			if bl == 1: #if only one is missing....
				f = taxon_string.index('')
				if f == 2:
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[order]
					parent_dict[order] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif f == 3:
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[class_]
					parent_dict[class_] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif f == 4:
					parent_dict[genus] = taxon_id[order]
					parent_dict[order] = taxon_id[class_]
					parent_dict[class_] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif f == 1:
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[order]
					parent_dict[order] = taxon_id[class_]
					parent_dict[class_] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif f == 7:
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[order]
					parent_dict[order] = taxon_id[class_]
					parent_dict[class_] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
			elif bl == 2: #if there are two missing....
				if taxon_string[2] == '' and taxon_string[3] == '':
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[2] == '' and taxon_string[4] == '':
					parent_dict[genus] = taxon_id[order]
					parent_dict[order] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[3] == '' and taxon_string[4] == '':
					parent_dict[genus] = taxon_id[class_]
					parent_dict[class_] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[0] == '' and taxon_string[1] == '':
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[order]
					parent_dict[order] = taxon_id[class_]
					parent_dict[class_] = ''
				elif taxon_string[1] == '' and taxon_string[2] == '':
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[order]
					parent_dict[order] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[1] == '' and taxon_string[3] == '':
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[class_]
					parent_dict[class_] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[1] == '' and taxon_string[4] == '':
					parent_dict[genus] = taxon_id[order]
					parent_dict[order] = taxon_id[class_]
					parent_dict[class_] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				else:
					print('check the #2 blank procedure') #a safe guard
					print(taxon)
			elif bl == 3: #if three are missing....
				if taxon_string[2] == '' and taxon_string[3] == '' and taxon_string[4] == '':
					parent_dict[genus] = taxon_id[phylum]
					parent_dict[phylum] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[1] == '' and taxon_string[3] == '' and taxon_string[4] == '':
					parent_dict[genus] = taxon_id[class_]
					parent_dict[class_] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[1] == '' and taxon_string[2] == '' and taxon_string[3] == '':
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[kingdom]
					parent_dict[kingdom] = ''
				elif taxon_string[0] == '' and taxon_string[1] == '' and taxon_string[2] == '':
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = taxon_id[order]
				else:
					print('check the #3 blank procedure') #a safe guard
					print(taxon)
			elif bl == 4: #if four are missing.....
				if taxon_string[0] != '':
					parent_dict[genus] = taxon_id[kingdom]
				else:
					parent_dict[genus] = taxon_id[family]
					parent_dict[family] = ''
			elif bl == 0: #this happens if no ranks are missing
				parent_dict[genus] = taxon_id[family]
				parent_dict[family] = taxon_id[order]
				parent_dict[order] = taxon_id[class_]
				parent_dict[class_] = taxon_id[phylum]
				parent_dict[phylum] = taxon_id[kingdom]
				parent_dict[kingdom] = ''
			elif bl == 5: #if five are missing....
				a = check_dict(genus, parent_dict)
				if a == False:
					parent_dict[genus] = ''
			else:
				print('new number of blanks') #a safe guard
				print(taxon) #keeps track of where I am
	print('dictionaries complete') #make sure the code gets to the end
	#creating all the output files for the TraitBank DwC-A
	#these file paths will be to your local machine
	out_file = open('/Volumes/PCCOMP/effechecka_country_results/' + country + '/tb_measurement.txt', 'w')
	out_file_t = open('/Volumes/PCCOMP/effechecka_country_results/' + country + '/tb_taxon.txt', 'w')
	out_file_c = open('/Volumes/PCCOMP/effechecka_country_results/' + country + '/tb_occurrence.txt', 'w')
	out_file.write('measurementID	occurrenceID	parentMeasurementID	measurementOfTaxon	measurementType	measurementValue	referenceID	contributor	source\n')
	out_file_t.write('taxonID	scientificName	parentNameUsageID	taxonRank\n')
	out_file_c.write('occurrenceID	taxonID\n')
	record_total = 0 #keeping track of the total number of records for each country
	in_file.seek(0)
	for line in in_file:
		line = line.strip('\n')
		row = line.split('\t')
		taxon_string = row[1].split('|') #the input file includes a pipe-delimited higher classification
		for i,j in enumerate(taxon_string): #this for loop removes any incertae sedis. We don't want that as a taxon.
			if j == 'incertae sedis':
				taxon_string[i] = ''
		taxon_string, r = norm_len(taxon_string) #using the function to normalize lengths
		if r == True:
			continue
		kingdom = taxon_string[0].title()
		phylum = taxon_string[1].title()
		class_ = taxon_string[2].title()
		order = taxon_string[3].title()
		family = taxon_string[4].title()
		genus = taxon_string[5].title()
		species = taxon_string[6]
		genus = genus_check(genus, species)
		if species == '' or genus == '': #if its not identified to species, then we don't want it
			continue
		else:
			taxon = genus + ' ' + species
			if taxon in taxa: #remove accidental duplication
				continue
			else:
				taxa.append(taxon)
				n = row[2] #this is our sample size
				polygon = polygons[geonames_id] #look up polygon for the country
				record_total = record_total + int(n) #keep running total of the number of records
				meas_id = 'M' + str(counter) #creating the measurement identifier
				t_id = taxon_id[taxon] #looking up taxon identifier
				occur_id = 'C' + t_id #creating the occurrence identifier
				par_id = parent_dict[taxon] #looking up the parent identifier
				#the below lines of output are writing to the darwin core files
				out_file.write(meas_id + '\t' + occur_id + '\t' + '' + '\t' + 'true' + '\t' + 'http://eol.org/schema/terms/Present' + '\t' + 'http://www.geonames.org/' + geonames_id + '\t' + 'R01|R02' + '\t' + 'Compiler: Anne E Thessen' + '\t' + 'http://gimmefreshdata.github.io/?limit=5000000&taxonSelector=' + taxon + '&traitSelector=&wktString=' + polygon + '\n')
				out_file.write('' + '\t' + '' '\t' + meas_id + '\t' + '' + '\t' + 'http://eol.org/schema/terms/SampleSize' + '\t' + str(n) + '\n')
				out_file_c.write(occur_id + '\t' + t_id + '\n')
				out_file_t.write(t_id + '\t' + taxon + '\t' + par_id + '\t' + 'species' + '\n')
				counter += 1
				#we need to keep a deduplicated list of the higher taxa so we can add them to the tb_taxon.txt file. 
				#Note that blanks are skipped.
				if genus in genera or genus == '':
					pass
				else:
					genera.append(genus)
				if family in families or family == '':
					pass
				else:
					families.append(family)
				if order in orders or order == '':
					pass
				else:
					orders.append(order)
				if class_ in classes or class_ == '':
					pass
				else:
					classes.append(class_)
				if phylum in phyla or phylum == '':
					pass
				else:
					phyla.append(phylum)
				if kingdom in kingdoms or kingdom == '':
					pass
				else:
					kingdoms.append(kingdom)

	#this is where we add the higher taxa to the tb_taxon.txt file
	for genus in genera:
		g_id = taxon_id[genus]
		p_id = parent_dict[genus]
		out_file_t.write(g_id + '\t' + genus + '\t' + p_id + '\t' + 'genus' + '\n')
	for family in families:
		f_id = taxon_id[family]
		p_id = parent_dict[family]
		out_file_t.write(f_id + '\t' + family + '\t' + p_id + '\t' + '' + '\n')
	for order in orders:
		o_id = taxon_id[order]
		p_id = parent_dict[order]
		out_file_t.write(o_id + '\t' + order + '\t' + p_id + '\t' + '' + '\n')
	for class_ in classes:
		c_id = taxon_id[class_]
		p_id = parent_dict[class_]
		out_file_t.write(c_id + '\t' + class_ + '\t' + p_id + '\t' + '' + '\n')
	for phylum in phyla:
		ph_id = taxon_id[phylum]
		p_id = parent_dict[phylum]
		out_file_t.write(ph_id + '\t' + phylum + '\t' + p_id + '\t' + '' + '\n')
	for kingdom in kingdoms:
		k_id = taxon_id[kingdom]
		p_id = ''
		out_file_t.write(k_id + '\t' + kingdom + '\t' + p_id + '\t' + '' + '\n')
	out_file_x.write(country + '\t' + geonames_id + '\t' + str(len(taxa)) + '\t' + str(record_total) + '\n') #output stats
	print('TB files complete') #make sure code gets to end
	#closing the input and output files for one country before moving on to the next
	in_file.close()
	out_file.close()
	out_file_t.close()
	out_file_c.close()
