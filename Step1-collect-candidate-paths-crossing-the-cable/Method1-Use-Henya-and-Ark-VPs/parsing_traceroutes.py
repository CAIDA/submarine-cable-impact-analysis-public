from dns import reversename
from datetime import datetime
import pyasn, os, time, sys, json, socket



def parsing_traceroutes_from_Vela_API(type, trace_detail, asndb, output_file, ASes_operating_the_cable, API_key):
    #traceroute is under the format: Country_src, id_measurement, src_probe, dst_probe, dest_IP, 'Country_dst', 'Traceroute'
    # E.g. ['BR', 592315, 'bfh-br', 'More_IPs-ao', '197.149.149.162', 'AO', 'Traceroute']
    command = "/usr/local/bin/python caida-tool-for-vela-api-usage.py --key " +  API_key + " get " + str(trace_detail[1]) + " > result.json"
    print (command)
    os.system(command)
    time.sleep(3)
    
    ## Parsing traceroute output
    wait = 0
    if type == 'trace' or type == 'Traceroute' or type == 'traceroute':
        result_fetched = ''
        with open(output_file, 'a') as fhg:
            with open('result.json', 'r') as fk:
                for line in fk:
                    if "values:" in line:
                        wait = 1
                    if '=' in line and wait == 1:
                        tab = line.split(' = ')
                        result_fetched = json.loads(tab[1])
                        #print(result_fetched)
        
            if result_fetched != '':
                fhg.write('%s\n' %(''))
                time_value = ' '
                if 1:
                    try:
                        timestampval = int(result_fetched["start"]["sec"])
                        hrfval = datetime.fromtimestamp(timestampval)
                        time_value = str(timestampval) + ' ('+ str(hrfval) + ')'
                    except:
                        pass
                
                if 'hops' in result_fetched:
                    k=0
                    to_print = "src=" + result_fetched['src'] + ' (' + trace_detail[0], trace_detail[2] + ')' + ' to ' + "dst=" + result_fetched['dst'] + '(' + trace_detail[5] + ')'
                    fhg.write('%s%s %s %s %s\n' %(time_value , ': Traceroute id ' , trace_detail[1] , ' from ', to_print))
                    
                    for elmt in result_fetched['hops']:
                        k+=1
                        ASN = asndb.lookup(str(elmt['addr']).strip())
                        try:
                            hostname = socket.gethostbyaddr(elmt['addr'])
                            hostname = hostname[0]
                        except:
                            try:
                                #hostname = Dict_hostnames[elmt['addr']]
                                hostname = reversename.from_address(elmt['addr'])
                            except:
                                hostname = ''
                
                        if str(ASN[0]).strip() not in ASes_operating_the_cable:
                            print (k, ' ', elmt['addr'],' (', hostname, ') ', elmt['rtt'],'ms AS', ASN[0], ' ', ASN[1])
                            toprint = str(k)+ ' '+ elmt['addr']+' ('+ str(hostname)  + ') '+ str(elmt['rtt']) +'ms    AS'+ str(ASN[0]).strip()+ ' '+ str(ASN[1])
                        else:
                            print (k, ' ', elmt['addr'],' (', hostname, ') ', elmt['rtt'],'ms AS', ASN[0], ' ', ASN[1]) , ' ==> via Cable Operating AS '
                            toprint = str(k)+ ' '+ elmt['addr']+' ('+ str(hostname)  + ') '+ str(elmt['rtt']) +'ms    AS'+ str(ASN[0]).strip()+ ' ' + str(ASN[1]) + ' ==> via Cable Operating AS '
                        
                        fhg.write('%s\n' %(toprint))
                    print()
                    return 1
            else:
                    return 0





if __name__ == "__main__":
    
    ## Initializations
    API_key = "YOUR-VELA-API-HERE"
    Dict_probes = {'AO': {'More_IPs-ao': ['197.149.149.162', '197.149.149.17']},
        'BR': {'More_IPs-br': ['177.159.62.125', '189.89.145.254', '200.187.0.104'],
            'bfh-br': [],
            'cgh-br': [u'170.238.234.65', u'170.238.232.57'],
            'gig-br': [u'200.159.254.167', u'200.143.240.49'],
            'poa2-br': [u'179.184.126.60', u'191.30.9.225'],
            'sao-br': [u'200.160.7.253', u'200.160.0.253']}}

    Results_to_fetch = [['BR', 592315, 'bfh-br', 'More_IPs-ao', '197.149.149.162', 'AO', 'Traceroute'], ['BR', 592316, 'bfh-br', 'More_IPs-ao', '197.149.149.17', 'AO', 'Traceroute'], ['BR', 592317, 'poa2-br', 'More_IPs-ao', '197.149.149.162', 'AO', 'Traceroute'], ['BR', 592318, 'poa2-br', 'More_IPs-ao', '197.149.149.17', 'AO', 'Traceroute'], ['BR', 592319, 'sao-br', 'More_IPs-ao', '197.149.149.162', 'AO', 'Traceroute'], ['BR', 592320, 'sao-br', 'More_IPs-ao', '197.149.149.17', 'AO', 'Traceroute'], ['BR', 592321, 'gig-br', 'More_IPs-ao', '197.149.149.162', 'AO', 'Traceroute'], ['BR', 592322, 'gig-br', 'More_IPs-ao', '197.149.149.17', 'AO', 'Traceroute'], ['BR', 592323, 'cgh-br', 'More_IPs-ao', '197.149.149.162', 'AO', 'Traceroute'], ['BR', 592324, 'cgh-br', 'More_IPs-ao', '197.149.149.17', 'AO', 'Traceroute']]

    i = 5

    asndb = pyasn.pyasn('../../Datastore/prefix2AS/20190101.prefix2as.dat')
    ASes_operating_the_cable = ['37468']
    
    while i > 0:
        for trace_detail in Results_to_fetch:
            delete = parsing_traceroutes_from_Vela_API('traceroute', trace_detail, asndb, 'result_full_mesh_traceroutes.txt', ASes_operating_the_cable, API_key)
            if delete == 1:
                Results_to_fetch.remove(trace_detail)
        i-=1

    print (Results_to_fetch)
