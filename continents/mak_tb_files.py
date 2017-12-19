import pickle
import re

continent_dict = {'africa':'6255146',
'europe':'6255148',
'asia':'6255147',
'oceania':'6255151',
'north america':'6255149',
'south america':'6255150'}

in_file = open('south_america.txt', 'r')
out_file = open('south_america_tb_measurement.txt', 'w')
out_file_t = open('south_america_tb_taxon.txt', 'w')
out_file_c = open('south_america_tb_occurrence.txt', 'w')
f = open('south_america_parent_dict.p', 'rb')
g = open('south_america_taxon_id.p', 'rb')

out_file.write('measurementID	occurrenceID	measurementOfTaxon	measurementType	measurementValue	referenceID	contributor	source\n')
out_file_t.write('taxonID	scientificName	parentNameUsageID	taxonRank\n')
out_file_c.write('occurrenceID	taxonID\n')

parents = pickle.load(f) #unpickles the dictionaries
ids = pickle.load(g)

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
    
kingdoms = []
phyla = []
classes = []
orders = []
families = []
taxa = []
genera = []
counter = 100000

record_total = 0
in_file.seek(0)
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
    species = taxon_string[6]
    if species == '' or genus == '': #if its not identified to species, then we don't want it
        continue
    else:
        taxon = genus + ' ' + species
        if taxon in taxa: #remove accidental duplication
            #print(taxon)
            continue
        else:
            taxa.append(taxon)
            meas_id = 'M' + str(counter)
            t_id = ids[taxon] #looking up taxon identifier
            occur_id = 'C' + t_id
            par_id = parents[taxon] #looking up the parent identifier
            #the below lines of output are writing to the darwin core files
            out_file.write(meas_id + '\t' + occur_id + '\t' + 'true' + '\t' + 'http://rs.tdwg.org/dwc/terms/continent' + '\t' + 'http://www.geonames.org/6255150' + '\t' + 'R01|R02' + '\t' + 'Compiler: Anne E Thessen' + '\t' + 'http://www.effechecka.org' + '\n')
            out_file_c.write(occur_id + '\t' + t_id + '\n')
            out_file_t.write(t_id + '\t' + taxon + '\t' + par_id + '\t' + 'species' + '\n')
            counter += 1
            #we need to keep a deduplicated list of the higher taxa so we can add them to the tb_taxon.txt file. Note that blanks are skipped.
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
print('total taxa ' + str(len(taxa))) #this prints the number of species measurements in the tb_measurements.txt file
#this is where we add the higher taxa to the tb_taxon.txt file
for genus in genera:
    g_id = ids[genus]
    p_id = parents[genus]
    out_file_t.write(g_id + '\t' + genus + '\t' + p_id + '\t' + 'genus' + '\n')
for family in families:
    f_id = ids[family]
    p_id = parents[family]
    out_file_t.write(f_id + '\t' + family + '\t' + p_id + '\t' + '' + '\n')
for order in orders:
    o_id = ids[order]
    p_id = parents[order]
    out_file_t.write(o_id + '\t' + order + '\t' + p_id + '\t' + '' + '\n')
for class_ in classes:
    c_id = ids[class_]
    p_id = parents[class_]
    out_file_t.write(c_id + '\t' + class_ + '\t' + p_id + '\t' + '' + '\n')
for phylum in phyla:
    ph_id = ids[phylum]
    p_id = parents[phylum]
    out_file_t.write(ph_id + '\t' + phylum + '\t' + p_id + '\t' + '' + '\n')
for kingdom in kingdoms:
    k_id = ids[kingdom]
    p_id = ''
    out_file_t.write(k_id + '\t' + kingdom + '\t' + p_id + '\t' + '' + '\n')
print('total records ' + str(record_total))
print('complete') #make sure code gets to end
        