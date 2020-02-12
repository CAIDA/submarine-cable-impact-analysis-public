#usr/bin/python
from pprint import pprint
import os, time, sys
import pycountry_convert as pc

#def fetch_AS_Nationality_from_ASrank_API(ASrank_url):



def fetch_list_Ark_probes(API_key, destinationfile):
    # fetches the list of Ark monitors,stores them into a file, and return the said list.
    command = "/usr/bin/python caida-tool-for-vela-api-usage.py --key " + API_key + " mons " + ' > ' + destinationfile
    run_command(command)
    
    List_probes = []
    beg = 0
    with open ( destinationfile, 'r') as fh:
        for line in fh:
            if 'by_country' in line:
                beg = 1
            if beg == 1 and '=' in line:
                line = line.strip()
                tab = line.split(' = ')
                probes = tab[1].split(',')
                List_probes += probes

print ("List_probes = ", list(set(List_probes)), len(list(set(List_probes))))
store_list_in_file (List_probes, destinationfile)
return list(set(List_probes))


def store_list_in_file (list_input, filename):
    # stores the content of a list of unique elements into a file, line by line.
    with open(filename, 'w') as fd:
        for elmt in list(set(list_input)):
            fd.write("%s \n" %(elmt))


def get_list_probes_from_file(file):
    ## reads the list of probes in a file and appends them to a python list
    List_probes = []
    with open(file, 'r') as fg:
        for line in fg:
            List_probes.append(line.strip())
    return List_probes


def classify_Ark_probes_per_continent(List_probes):
    ## Classifies Ark probes per continent and stores them into corresponding files
    Dict_cont_probe = {}
    continents = {
    'NA': 'North_America',
    'SA': 'South_America',
    'AS': 'Asia',
    'OC': 'Oceania_Australia',
    'AF': 'Africa',
    'EU': 'Europe'
    }
    i = 0
    for probe in List_probes:
        tab = probe.split('-')
        cont = ''
        try:
            cont = pc.country_alpha2_to_continent_code(str(tab[1]).upper())
        #i+=1
        except:
            if str(tab[1]).upper() == 'UK':
                cont = 'EU'
            #i+=1
            pass
        print ("The probe " + probe + " is in " + cont)
        
        ## store in a dictionary
        if continents[cont] in Dict_cont_probe:
            Dict_cont_probe[continents[cont]].append(probe)
else:
    Dict_cont_probe[continents[cont]]= []
    Dict_cont_probe[continents[cont]].append(probe)
    #print "i = ", i
    #pprint(Dict_cont_probe)
    return Dict_cont_probe


#def prefix2AS():




def run_command(command):
    print('\n', command)
    os.system(command)
    time.sleep(3)


if __name__ == "__main__":
    
    ## Initializations:
    ## Add your Vela API key below.
    folder = '../List_Ark_probes'
    API_key = "YOUR-API-KEY-HERE"
    destinationfile = '/list_probes_API.txt'
    
    ## Fetch list Ark probes.
    List_Ark_probes = fetch_list_Ark_probes(API_key, folder + destinationfile)
    
    ## Classify probes per continents
    Dictionary_probes_per_continents = classify_Ark_probes_per_continent(List_Ark_probes)
    for continent in Dictionary_probes_per_continents:
        destinationfolder = '../Probes_by_continent/'
        destinationfile = destinationfolder + continent
        store_list_in_file (Dictionary_probes_per_continents[continent], destinationfile)
