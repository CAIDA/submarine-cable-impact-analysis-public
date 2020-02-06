## This script will run traceroutes with the vela API between Ark probes in the countries linked by the cable.

## Requirements: The execution of this script requires the installation of the IPy (https://pypi.org/project/IPy/)
## and that of the dnspython (https://pypi.org/project/dnspython/) packages
from IPy import IP
from dns import reversename
from datetime import datetime
from pprint import pprint
from parsing_traceroutes import *
import os, time, sys, json, pyasn, socket

def get_list_probes(file):
    ## reads the list of probes in the file and appends them to a python list
    List_probes = []
    with open(file, 'r') as fg:
        for line in fg:
            List_probes.append(line.strip())
    return List_probes


def extract_set_probes_on_both_sides_of_link (Ark_probes, Countries_linked):
    ## identifies the probes whose names contain the country codes of the countries interconnected by the studied cable
    Group_probes = {}
    for probe in Ark_probes:
        for CC in Countries_linked:
            if CC not in Group_probes:
                Group_probes[CC] = []
            if '-'+ CC.lower() in probe:
                Group_probes[CC].append(probe)
    return Group_probes


def run_command(command):
    print('\n', command)
    os.system(command)
    time.sleep(3)


def fetch_and_get_first_public_IP(measID, probe, DestinationIP, type,  API_key):
    command = "/usr/local/bin/python caida-tool-for-vela-api-usage.py --key 374bcf659bfcfec092b71c0736c5e5fc get " + str(measID) + " > " + sub_folder + "/result.json"
    print (command)
    os.system(command)
    time.sleep(3)
    
    first_public_IP = []
    wait = 0
    if type == 'trace' or type == 'Traceroute' or type == 'traceroute':
        with open(sub_folder + '/result.json', 'r') as fk:
            for line in fk:
                if "values:" in line:
                    wait = 1
                if '=' in line and wait == 1:
                    tab = line.split(' = ')
                    data = json.loads(tab[1])
                    if "hops" in data.keys():
                        for elmt in data["hops"]:
                            if '.' in elmt["addr"]:
                                ip = IP(str(elmt["addr"]))
                                #print elmt["addr"], ip, ip.iptype()
                                if ip.iptype() == 'PUBLIC' and len(first_public_IP) <2:
                                    first_public_IP.append(elmt['addr'])

        print ('Result: List_IPs = ', probe , first_public_IP)
        return {"Pb":probe, "IPs":first_public_IP}



if __name__ == "__main__":
    
    ## Create folders.
    sub_folder = 'intermediate_files'
    command = 'mkdir ' + sub_folder
    os.system(command)
    
    result_folder = 'results'
    command = 'mkdir ' + result_folder
    os.system(command)
    
    ## Initializations
    API_key = "YOUR-VELA-API-HERE"
    ##Extension: One could randomly pick the destination IP from this list.
    ##potential_destination_IPs = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
    
    ## These countries can be changed depending on the cable under study.
    Countries_linked = ['BR', 'AO']
    
    ## Create an initial list of IPs known to be located within the countries on both sides of the cable (Example:
    ## could include public IPs of RIPE Atlas probes)
    List_destination_IPs_CountryA = ['177.159.62.125', '189.89.145.254', '200.187.0.104']
    List_destination_IPs_CountryB = ['197.149.149.162', '197.149.149.17']
    ## 197.149.149.162 => pe2-nc026.ang.sgn.as37468.angolacables.ao => router connected to AS37468 Looking glass.
    
    
    ## This file location can be modified by the user to input another file.
    file_list_probes = "../../Datastore/list_probes.txt"
    
    if os.path.exists(file_list_probes):
        Ark_probes = get_list_probes(file_list_probes)
        print(Ark_probes, len(Ark_probes), '\n')
        
        ## We then pick the probes in the selected countries
        Probes_on_both_sides_of_cable = extract_set_probes_on_both_sides_of_link (Ark_probes, Countries_linked)
        pprint(Probes_on_both_sides_of_cable)

    else:
        ## Use Vela API to find the list of Ark probes and create the list_probes.txt file
        command = "/usr/local/bin/python caida-tool-for-vela-api-usage.py --key " + API_key + " mons " + ' > ' + sub_folder + '/list_probes_API.txt'
        run_command(command)

        List_probes = []
        beg = 0
        with open ('list_probes_API.txt', 'r') as fh:
            for line in fh:
                if 'by_country' in line:
                    beg = 1
                if beg == 1 and '=' in line:
                    line = line.strip()
                    tab = line.split(' = ')
                    probes = tab[1].split(',')
                    List_probes += probes

        print ("List_probes = ", list(set(List_probes)), len(list(set(List_probes))))

        with open (file_list_probes, 'a') as fk:
            for probe in list(set(List_probes)):
                fk.write("%s\n" %(probe))

        ## We then pick the probes in the selected countries
        Probes_on_both_sides_of_cable = extract_set_probes_on_both_sides_of_link (list(set(List_probes)), Countries_linked)

    #print( 'Probes_on_both_sides_of_cable = ', Probes_on_both_sides_of_cable)


    ## Build a dictionary with as keys CC, their corresponding probes and as values IPs
    Dict_CC_probes_IPs = {}
    Cases_to_retry = []

    if os.path.exists(sub_folder +'/traceroutes_tests_with_Ark.txt'):
        pass
    else:
        with open(sub_folder +'/traceroutes_tests_with_Ark.txt', 'a') as fj:
            fj.write("%s; %s; %s; %s; %s; %s\n" %('Type measearement', 'Timestamp', 'Datetime', 'Probe', 'Destination IP', 'Meas ID'))
            fj.close()

    for Country in Probes_on_both_sides_of_cable:
        print ('Considered country = ', Country)
        if Country not in Dict_CC_probes_IPs:
            Dict_CC_probes_IPs[Country] = {}
        
        for probe in Probes_on_both_sides_of_cable[Country]:
            print ('Considering probe = ', probe)
            if probe not in Dict_CC_probes_IPs[Country]:
                Dict_CC_probes_IPs[Country][probe] = []
            
            ## Launch traceroute
            command = "/usr/local/bin/python caida-tool-for-vela-api-usage.py --key " +  API_key + " trace " + probe + ' ' + '8.8.8.8' + ' > ' + sub_folder +'/output_run.txt'
            print ('Launching traceroute => ', command)
            os.system(command)
            nowval = datetime.now()
            timestampval = time.time()
            time.sleep(3)
            
            ## Get traceroute ID
            value = 0
            with open(sub_folder +'/traceroutes_tests_with_Ark.txt', 'a') as fj:
                with open(sub_folder + '/output_run.txt', 'r') as fgh:
                    for elmt1 in fgh:
                        if 'result ID:' in elmt1:
                            value = int(elmt1[elmt1.find(':')+1:])
                            print(value)
                            # 'Type measurement', 'Timestamp', 'Datetime', 'Probe', 'Destination IP', 'Meas ID'
                            fj.write("%s; %s; %s; %s; %s; %s\n" %('Traceroute', timestampval, nowval, probe, '8.8.8.8', value))

                            ## Parse traceroute and get first public IP of the router linked to the gateway of the network in which the probe is hosted
                            if int(value) != 0:
                                first_public_IP_probe = fetch_and_get_first_public_IP(value, probe, '8.8.8.8', 'Traceroute', API_key)

                                if len(first_public_IP_probe["IPs"])>0:
                                    Dict_CC_probes_IPs[Country][probe] = first_public_IP_probe["IPs"]

                                else:
                                    Cases_to_retry.append([Country, value, probe, '8.8.8.8', 'Traceroute'])
                                    

    pprint(Dict_CC_probes_IPs)
    
    print()
    print()
    print('Cases_to_retry = ', Cases_to_retry)

    ## Try to find IPs again.
    i = 5
    while i>0:
        print ('Turn ', i)
        for case in Cases_to_retry:
            if len(Dict_CC_probes_IPs[case[0]][case[2]]) == 0:
                print ('case =', case)
                first_public_IP_probe = fetch_and_get_first_public_IP(case[1], case[2], case[3], case[4], API_key)
                
                if len(first_public_IP_probe["IPs"])>0:
                    Dict_CC_probes_IPs[case[0]][case[2]] = first_public_IP_probe["IPs"]
                    del(case)
        i-=1

    #pprint(Dict_CC_probes_IPs)

    ## Add IPs known to be on both sides of the cable (Eg. IPs of RIPE Atlas probes/anchors):
    Dict_CC_probes_IPs[Countries_linked[0]]["More_IPs-br"] = List_destination_IPs_CountryA
    Dict_CC_probes_IPs[Countries_linked[1]]["More_IPs-ao"] = List_destination_IPs_CountryB

    ## Launch full mesh measurements between Arch probes.
    pprint(Dict_CC_probes_IPs)

    if os.path.exists('full_mesh_traceroutes_with_Ark.txt'):
        pass
    else:
        with open('full_mesh_traceroutes_with_Ark.txt', 'a') as fj:
            fj.write("%s; %s; %s; %s; %s; %s; %s; %s; %s\n" %('Type measurement', 'Timestamp', 'Datetime', 'Src_Probe', 'Src_Country', 'Destination_Probe', 'Destination_IP', 'Destination_Country', 'Meas ID'))
            fj.close()

    Results_to_fetch = []

    for Country_src in Dict_CC_probes_IPs:
        print('Country_src = ', Country_src)
        list_probes = Dict_CC_probes_IPs[Country_src].keys()
        for src_probe in list_probes:
            for Country_dst in Dict_CC_probes_IPs:
                if Country_dst != Country_src:
            
                    for dst_probe in Dict_CC_probes_IPs[Country_dst]:
                        if len(Dict_CC_probes_IPs[Country_dst][dst_probe]) >=0:
                            for dest_IP in Dict_CC_probes_IPs[Country_dst][dst_probe]:
                                
                                #print('dst_probe = ', dst_probe)
                                if '-' + Country_src.lower() not in dst_probe and  "More_IPs" not in src_probe:
                                    #current_CC = dst_probe.split('-')
                                    #current_CC = current_CC.upper()
                                    
                                    command = "/usr/local/bin/python caida-tool-for-vela-api-usage.py --key " +  API_key + " trace " + src_probe + ' ' + dest_IP + ' > ' + sub_folder + '/output_run.txt'
                                    print ('Launching traceroute => ', command)
                                    os.system(command)
                                    nowval = datetime.now()
                                    timestampval = time.time()
                                    time.sleep(5)
                    
                                    ## Get traceroute ID
                                    value = 0
                                    with open('full_mesh_traceroutes_with_Ark.txt', 'a') as fj:
                                        with open(sub_folder +'/output_run.txt', 'r') as fgh:
                                            for elmt1 in fgh:
                                                if 'result ID:' in elmt1:
                                                    value = int(elmt1[elmt1.find(':')+1:])
                                                    print(value)
                                                    # 'Type measurement', 'Timestamp', 'Datetime', 'Probe', 'Destination Probe','Destination IP', 'Meas ID'
                                                    fj.write("%s; %s; %s; %s; %s; %s; %s; %s; %s\n" %('Traceroute', timestampval, nowval, src_probe, Country_src, dst_probe, dest_IP, Country_dst, value))
                                                    Results_to_fetch.append([Country_src, value, src_probe, dst_probe, dest_IP, Country_dst, 'Traceroute'])

    print()
    print()
    pprint(Dict_CC_probes_IPs)

    ''' Example: {'AO': {'More_IPs-ao': ['197.149.149.162', '197.149.149.17']},
    'BR': {'More_IPs-br': ['177.159.62.125', '189.89.145.254', '200.187.0.104'],
    'bfh-br': [],
    'cgh-br': [u'170.238.234.65', u'170.238.232.57'],
    'gig-br': [u'200.159.254.167', u'200.143.240.49'],
    'poa2-br': [u'179.184.126.60', u'191.30.9.225'],
    'sao-br': [u'200.160.7.253', u'200.160.0.253']}}
    '''

    print()
    print()
    print (Results_to_fetch)

    ### Parsing results and redirecting them in the file
    i = 5
    asndb = pyasn.pyasn('../../Datastore/prefix2AS/20190101.prefix2as.dat')
    ASes_operating_the_cable = ['37468']

    while i > 0:
        for trace_detail in Results_to_fetch:
            delete = parsing_traceroutes_from_Vela_API('traceroute', trace_detail, asndb, result_folder+'/result_full_mesh_traceroutes.txt', ASes_operating_the_cable, API_key)
            if delete == 1:
                Results_to_fetch.remove(trace_detail)
        i-=1
        time.sleep(3)

    print ("These are the measurements that we were not able to parse because of the absence of outputs:", Results_to_fetch)
