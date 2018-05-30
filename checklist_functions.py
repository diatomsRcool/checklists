#all of these functions were written for use in handline output from effechecka and 
#making TraitBank files from effechecka output


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
#lengths. The 'skip' variable helps us know if we need to skip a row due to insufficient taxonomic information
def norm_len(hi_class):
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