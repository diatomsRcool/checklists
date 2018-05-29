#this code makes the dictionaries we need to build the TraitBank file

import pickle

n = 'australia'

in_file = open('/Volumes/PCCOMP/effechecka_country_results/' + n + '/' + n + '.tsv', 'r')

#this function checks the parent of a taxon to see if it is blank. The purpose of this function is to avoid replacing
#a named parent with a blank if a data record just happens to be missing its parent
def check_dict(name, dictp):
	if name in dictp: 
		if dictp[name] != '':
			check = True
		else:
			check = False
	else:
		check = False
	return check

#this function normalizes the length of the pipe-delimited higher classification so the rest of the code will work.
#I noticed in the Australia and Argentina lists, instead of having blanks, the higher classifications were different 
#lengths.
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
			if genus == 'X':
				skip = True
			else:
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


#I wrote this function to fix a common error in the genus names. This error comes from the data source.
def genus_check(genus, species):
	r = genus.split(' ')
	if len(r) > 1:
		if r[1] == "f." or r[1] == "F." or r[1].lower() == species or r[1] == 'Delle' or r[1] == 'Des' or r[1] == 'Den':
			genus = r[0]
			return(genus)
		else:
			return(genus)
	else:
		return(genus)


counter = 100000
kingdoms = []
phyla = []
classes = []
orders = []
families = []
genera = []
species = []
parent_dict = {}
taxon_id = {}
next(in_file)
for line in in_file:
	line = line.strip('\n')
	row = line.split('\t')
	taxon_string = row[1].split('|') #the json result includes a pipe-delimited higher classification
	for i,j in enumerate(taxon_string): #this for loop removes any incertae sedis. We don't want that as a taxon.
		if j == 'incertae sedis':
			taxon_string[i] = ''
	taxon_string, r = norm_len(taxon_string) #using the function to normalize lengths
	if r == True:
		continue
	#print(taxon_string)
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
		if taxon in species: #this gets rid of some duplication that sneaks into the effechecka results due to slight differences in the name strings
			pass
		else:
			species.append(taxon) #giving each taxon an identifier from here to line 66
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
		if bl == 1: #from here to line 124 deals with missing ranks. The exact strategy for dealing with the problem depends on how many and which ones are missing
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
		elif bl == 2:
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
		elif bl == 3:
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
		elif bl == 4:
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
		elif bl == 5:
			a = check_dict(genus, parent_dict)
			if a == False:
				parent_dict[genus] = ''
		else:
			print('new number of blanks') #a safe guard
			print(taxon) #keeps track of where I am

pickle.dump(parent_dict, open('parent_dict.p', 'wb'))
pickle.dump(taxon_id, open('taxon_id.p', 'wb'))
print('complete') #make sure the code gets to the end