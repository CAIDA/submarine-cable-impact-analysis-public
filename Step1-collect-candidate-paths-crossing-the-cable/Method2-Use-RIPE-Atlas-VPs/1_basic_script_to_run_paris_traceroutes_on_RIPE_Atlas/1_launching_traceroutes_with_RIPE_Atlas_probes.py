## Goal:
## This is a test (#Python) script, which could be used to
## launch RIPE Atlas full-mesh traceroutes between a set of
## probes in two countries or from a set of random probes
## selected worldwide toward in those located in a country.



## Launching traceroutes from Angola to Brazil (vice versa)
import os, time, sys, random, json, datetime, time
try:
    import urllib2
except:
    import urllib.request as urllib2


## Initializations
start_time = time.time()
start_time_hrf = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
print ("start_time_hrf = ", start_time_hrf)
Output_folder =  "Measurements_infos/"
## For this paper, we used the following line
#Both_Countries = ['AO', 'BR']
Both_Countries = ['CM', 'BR']
protocols = ['ICMP', 'UDP']

## Full mesh traceroutes or WW towards country traceroutes.
Full_mesh_traceroutes = 1
Traceroutes_WW_Country = 1
A_targeted_IP_in_CountryA = "152.238.248.1"

## Creating List Measurements Folder
try:
    os.mkdir(Output_folder)
except:
    pass


## Getting list and all details about the probes in the first country i.e. Angola - AO
CountryA = Both_Countries[0]
url_CountryA = 'https://atlas.ripe.net/api/v2/probes/?limit=100&country_code=' + CountryA
print ('CountryA = ', Both_Countries[0])
print ('url_CountryA = ', url_CountryA)
usock = urllib2.urlopen(url_CountryA)
data2 = usock.read()
usock.close()
##print(data2)


filename = Output_folder + "list_probe_" + CountryA + ".json"
with open(filename , "w") as ffa:
    ffa.write('%s' %(data2))
    ffa.close()

json_data = open(filename)
data2_loaded = ''
data2_loaded = json.load(json_data)



Dict_probes_CountryA = {}
i= -1
while i+1< len(data2_loaded['results']):
    i+=1
    #print()
    if data2_loaded['results'][i]['status']['name'] == 'Connected' and data2_loaded['results'][i]['address_v4'] != None:
        #print (data2_loaded['results'][i])
        #print (data2_loaded['results'][i]['id'], data2_loaded['results'][i]['country_code'], data2_loaded['results'][i]['geometry']['coordinates'], data2_loaded['results'][i]['address_v4'], data2_loaded['results'][i]['asn_v4'])
        Dict_probes_CountryA[str(data2_loaded['results'][i]['id'])] = [data2_loaded['results'][i]['id'], data2_loaded['results'][i]['country_code'], data2_loaded['results'][i]['geometry']['coordinates'], data2_loaded['results'][i]['address_v4'], str(data2_loaded['results'][i]['asn_v4'])]
print ()
print ("Dict_probes_CountryA = ", Dict_probes_CountryA, len (Dict_probes_CountryA.keys()))



## Getting list and all details about the probes in the first country i.e. Brazil - BR
CountryB = Both_Countries[1]
url_CountryB = 'https://atlas.ripe.net/api/v2/probes/?limit=100&country_code=' + CountryB
print ('CountryB = ', Both_Countries[1])
print ('url_CountryB = ', url_CountryB)
usock = urllib2.urlopen(url_CountryB)
data2 = usock.read()
usock.close()
##print(data2)

filename = Output_folder + "list_probe_" + CountryB + ".json"
with open(filename , "w") as ffa:
    ffa.write('%s' %(data2))
    ffa.close()

json_data=open(filename)
data2_loaded = ''
data2_loaded = json.load(json_data)


Dict_probes_CountryB = {}
i= -1
while i+1< len(data2_loaded['results']):
    i+=1
    #print()
    if data2_loaded['results'][i]['status']['name'] == 'Connected' and data2_loaded['results'][i]['address_v4'] != None:
        #print (data2_loaded['results'][i])
        #print (data2_loaded['results'][i]['id'], data2_loaded['results'][i]['country_code'], data2_loaded['results'][i]['geometry']['coordinates'], data2_loaded['results'][i]['address_v4'], data2_loaded['results'][i]['asn_v4'])
        Dict_probes_CountryB[str(data2_loaded['results'][i]['id'])] = [data2_loaded['results'][i]['id'], data2_loaded['results'][i]['country_code'], data2_loaded['results'][i]['geometry']['coordinates'], data2_loaded['results'][i]['address_v4'], str(data2_loaded['results'][i]['asn_v4'])]
print ()
print ("Dict_probes_CountryB = ", Dict_probes_CountryB, len(Dict_probes_CountryB.keys()))



if os.path.exists('Final_List_measurements.txt'):
    print ('File exists')
else:
    with open ('Final_List_measurements.txt', 'a') as fg:
        fg.write ("%s; %s; %s; %s; %s; %s; %s; %s; %s\n" %('Timestamp', 'Datetime', 'ID_meas', 'Probe destination ID', 'IP destination', 'CC_destination', 'Probe Source IDs', 'CC_source', 'protocol'))


## Launching full-mesh ICMP/UDP paris-traceroutes measurements
if Full_mesh_traceroutes:
    
    for protocol in protocols:

        ### Launching measurements from probes in CountryA
        for key_CountryA in Dict_probes_CountryA:
            value = len(Dict_probes_CountryB.keys())
            value = str(value).strip()
            
            command = """curl --dump-header - -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d """ +  "\'" + """ {"definitions":[{"target": " """ + Dict_probes_CountryA[key_CountryA][3] + """ ", "af": 4, "timeout": 4000,"description": "Traceroute measurement from all probes in """ + CountryB + """ to """ + Dict_probes_CountryA[key_CountryA][3] + """ (""" + CountryA + """, AS"""
            
            command +=  Dict_probes_CountryA[key_CountryA][4] +  """ )","protocol": \"""" + protocol + """\","resolve_on_probe": false,"packets": 3,"size": 48,"first_hop": 1,"max_hops": 32,"paris": 16,"destination_option_size": 0,"hop_by_hop_option_size": 0,"dont_fragment": false,"skip_dns_check": false,"type": "traceroute","is_public": false}],"probes": [{"value": " """

            command += str(','.join(Dict_probes_CountryB.keys()))  + """ ","type": "probes","requested": """
            
            command += str(len(Dict_probes_CountryB.keys())) + """}],"is_oneoff": true,"bill_to": "RIPEAtlasusername@mail.org"} ' https://atlas.ripe.net/api/v2/measurements//?key=YOUR-API-KEY"""
                        
            command += """ > test.txt"""
            command = command.replace("\'", "'")
            print
            print command
            
            ### Running traceroutes
            os.system(command)
            
            ### Parsing output and getting the ID of the traceroutes
            print ('Parsing output')
            value1 = ''
            with open ('test.txt', 'r') as fjj:
                for line11 in fjj:
                    if 'error' not in line11 and 'measurements' in line11 :
                        value1 = str(line11[17:-2]).strip()
                        if value1 != "":
                            with open ('Final_List_measurements.txt', 'a') as fg:
                                #Timestamp, Datetime, ID_meas, Probe destination ID, IP destination, CC_destination, Probe Source IDs, CC_source
                                fg.write ("%s; %s; %s; %s; %s; %s; %s; %s; %s\n" %(start_time, start_time_hrf, value1, key_CountryA,  Dict_probes_CountryA[key_CountryA][3], Dict_probes_CountryA[key_CountryA][1], '-'.join(Dict_probes_CountryB.keys()), CountryB, protocol))


        ### Launching measurements from country B
        for key_CountryB in Dict_probes_CountryB:
            time.sleep(5)
            value = len(Dict_probes_CountryA.keys())
            value = str(value).strip()
            
            command = """curl --dump-header - -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"definitions": [{"target": " """ + Dict_probes_CountryB[key_CountryB][3] + """ ","af": 4, "timeout": 4000, "description": "Traceroute measurement from all probes in """ + CountryA + """ to """ + Dict_probes_CountryB[key_CountryB][3] + """ (""" + CountryB + """, AS"""
                
            command +=  Dict_probes_CountryB[key_CountryB][4] +  """)", "protocol":  \"""" + protocol + """\", "resolve_on_probe": false, "packets": 3, "size": 48, "first_hop": 1, "max_hops": 32, "paris": 16, "destination_option_size": 0, "hop_by_hop_option_size": 0, "dont_fragment": false, "skip_dns_check": false, "type": "traceroute", "is_public": false}], "probes": [{"value": " """
            
            if len( Dict_probes_CountryA.keys()) > 1:
                command += str(','.join(Dict_probes_CountryA.keys()))  + """ ", "type": "probes", "requested":  """
            
            elif len( Dict_probes_CountryA.keys()) == 1:
                A = Dict_probes_CountryA.keys()
                command += str(A[0])  + """ ", "type": "probes", "requested":  """

                command += str(len(Dict_probes_CountryA.keys())) + """}], "is_oneoff": true, "bill_to": "RIPEAtlasusername@mail.org"}""" + "'" +""" https://atlas.ripe.net/api/v2/measurements//?key=YOUR-API-KEY"""

                command += """ > test.txt"""
            print
            print ('command = ', command)
            
            if len(Dict_probes_CountryA.keys()) >0:
                command = command.replace("\'", "'")
                print command
                os.system(command)
                
                ### Parsing output and getting the ID of the traceroutes
                value1 = ''
                with open ('test.txt', 'r') as fjj:
                    for line11 in fjj:
                        if 'error' not in line11 and 'measurements' in line11 :
                            value1 = str(line11[17:-2]).strip()
                            if value1 != "":
                                with open ('Final_List_measurements.txt', 'a') as fg:
                                    #Timestamp, Datetime, ID_meas, Probe destination ID, IP destination, CC_destination, Probe Source IDs, CC_source
                                    
                                    if len( Dict_probes_CountryA.keys()) > 1:
                                        #print ()
                                        #print (start_time, start_time_hrf, value1, key_CountryB,  Dict_probes_CountryB[key_CountryB][3], Dict_probes_CountryB[key_CountryB][1], '-'.join(Dict_probes_AO.keys()), 'AO', protocol)
                                        fg.write ("%s; %s; %s; %s; %s; %s; %s; %s; %s\n" %(start_time, start_time_hrf, value1, key_CountryB,  Dict_probes_CountryB[key_CountryB][3], Dict_probes_CountryB[key_CountryB][1], '-'.join(Dict_probes_CountryA.keys()), CountryA, protocol))
                                    
                                    elif len( Dict_probes_CountryA.keys()) == 1:
                                        A = Dict_probes_CountryA.keys()
                                        #print ()
                                        #print (start_time, start_time_hrf, value1, key_CountryB,  Dict_probes_CountryB[key_CountryB][3], Dict_probes_CountryB[key_CountryB][1], str(A[0]), CountryA, protocol)
                                        fg.write ("%s; %s; %s; %s; %s; %s; %s; %s; %s\n" %(start_time, start_time_hrf, value1, key_CountryB,  Dict_probes_CountryB[key_CountryB][3], Dict_probes_CountryB[key_CountryB][1], str(A[0]), CountryA, protocol))

    
        print
        ### From the World to BR
        if Traceroutes_WW_Country:
            command = """curl --dump-header - -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"definitions": [{"target": " """ + A_targeted_IP_in_CountryA + """ ","af": 4, "timeout": 4000, "description": "Traceroute measurement from  WW towards an IP (""" + A_targeted_IP_in_CountryA + """) in """ + CountryA + """ " ,"protocol": "ICMP","resolve_on_probe": false, "packets": 3, "size": 48, "first_hop": 1, "max_hops": 32, "paris": 16, "destination_option_size": 0, "hop_by_hop_option_size": 0,"dont_fragment": false,"skip_dns_check": false,"type": "traceroute","is_public": false}],"probes": [{"tags": {"include": [],"exclude": []},"type": "area","value": "West","requested": 10},{"tags": {"include": [],"exclude": []},"type": "area","value": "North-Central","requested": 10},{"tags": {"include": [],"exclude": []},"type": "area","value": "South-Central","requested": 10},{"tags": {"include": [],"exclude": []},"type": "area","value": "North-East","requested": 10},{"tags": {"include": [],"exclude": []},"type": "area","value": "South-East","requested": 10}],"is_oneoff": true,"bill_to": "RIPEAtlasusername@mail.org"}' https://atlas.ripe.net/api/v2/measurements//?key=YOUR-API-KEY"""
            
            command += '> test2.txt'
            
            command = command.replace("\'", "'")
            os.system(command)
            
            print ('command = ', command)
            
            ### Parsing output and getting the ID of the traceroutes
            value1 = ''
            with open ('test.txt', 'r') as fjj:
                for line11 in fjj:
                    if 'error' not in line11 and 'measurements' in line11 :
                        value1 = str(line11[17:-2]).strip()
                        if value1 != "":
                            with open ('Final_List_measurements.txt', 'a') as fg:
                                #Timestamp, Datetime, ID_meas, Probe destination ID, IP destination, CC_destination, Probe Source IDs, CC_source
                                fg.write ("%s; %s; %s; %s; %s; %s; %s; %s; %s\n" %(start_time, start_time_hrf, value1, '', A_targeted_IP_in_CountryA, CountryA, 'World','WW', protocol))
