from datetime import datetime
import time
import glob, time, os, sys, json
import pyasn

## Load dns names
Dict_hostnames = {}
with open ('DNS_names_all_IPs/Unik_AO_BR_Jan2018_Sept2018_NT_all_IPs.hostnames', 'r') as fg:
	for line in fg:
	    if 'FAIL' not in line:
		#print line
		tab = line.strip().split('\t')
		print tab
		if len(tab) > 2:
			Dict_hostnames[tab[1]] = tab[2]

asndb = pyasn.pyasn('/home/roderick/CAIDA_Work/20_launch_meas_with_Vela/General_infos/data_files/20190501.prefix2as.dat')

#while 1:
## Build list of parsed files:
List_parsed_outputs =[]
with open ('parsed.txt', 'r') as fkk:
	for line in fkk:
		List_parsed_outputs.append(line.strip())


if 1:
   folders = glob.glob('Graph3/*')

   for elmt in folders:
	list_pairs = glob.glob(elmt + '/IDs_meas_*')
	print list_pairs

	for file in list_pairs:
		with open(file, 'r') as fh:
		    file_to_open = file.replace('IDs_meas', 'Outputs_meas')

		    with open(file_to_open, 'a') as fhg:
			for line in fh:
			    if file + '; ' + line.strip() not in List_parsed_outputs:
				#fhg.write('%s\n' %(''))
				print line
				#fhg.write('%s\n' %(line))
				tab = line.split('; ')

				if int(tab[-1]) > 0:
					fhg.write('%s\n' %(''))
					fhg.write('%s\n' %(line.strip()))
					value = str(tab[-1]).strip()
					command2 = "python vela-api.py --key 374bcf659bfcfec092b71c0736c5e5fc get " + str(value) + " > result.json" 
					os.system(command2)
					#print command2
					#sys.exit('OUT')
					time.sleep(0.5)

					result_fetched = ''
					with open('result.json', 'r') as f:
						for line1 in f:
						    if ' = ' in line1:
							val = line1.split(' = ')
							result_fetched = json.loads(val[1])

					if result_fetched != '':
					   if 'hops' in result_fetched:
						k=0

						#print result_fetched
						to_print = "src=" + result_fetched['src'] + ' ' + "dst=" + result_fetched['dst']
						fhg.write('%s\n' %(to_print))

						print
						#u'src': u'119.40.82.245', u'hoplimit': 0, u'stop_reason': u'GAPLIMIT', u'hop_count': 21, u'dst': u'104.255.216.79', u'userid': 0, u'stop_data': 0, u'firsthop': 1, u'start': {u'usec': 516244, u'ftime': u'2019-06-26 03:37:32', u'sec': 1561520252
						for elmt in result_fetched['hops']:
							k+=1
							#print elmt['src'], elmt['dst']
							ASN = asndb.lookup(str(elmt['addr']).strip())

							try:
								hostname = Dict_hostnames[elmt['addr']]
							except:
								hostname = ''


							if str( elmt['addr']).strip() ==  '170.238.232.145' or str( elmt['addr']).strip() ==  '170.238.232.149'  or  str( elmt['addr']).strip() ==  '170.238.232.146'  or  str( elmt['addr']).strip() ==  '170.238.232.150':  
								print k, ' ', elmt['addr'],' (', hostname, ') ', elmt['rtt'],'ms AS', ASN[0], ' ', ASN[1], 'VIA_SACS'
								toprint = str(k)+ ' '+ elmt['addr']+' ('+ hostname+ ') '+ str(elmt['rtt']) +'ms    AS'+ str(ASN[0]).strip()+ ' ' + str(ASN[1])+ ' ==>VIA_SACS'
							else:
								print k, ' ', elmt['addr'],' (', hostname, ') ', elmt['rtt'],'ms AS', ASN[0], ' ', ASN[1]
								toprint = str(k)+ ' '+ elmt['addr']+' ('+ hostname+ ') '+ str(elmt['rtt']) +'ms    AS'+ str(ASN[0]).strip()+ ' '+ str(ASN[1])

							fhg.write('%s\n' %(toprint))


					with open('parsed.txt', 'a') as fj:
						List_parsed_outputs.append(file + '; ' + line.strip())
						fj.write('%s; %s\n' %(file, line.strip()))


				#nowval = datetime.now()
				#timestampval = time.time()
				## Get the results
				#if value != 0:
				#	command2 = "python vela-api.py --key 374bcf659bfcfec092b71c0736c5e5fc get " + str(value) + " > result.json" 
				#	os.system(command2)
                                #	time.sleep(3)

				## Transform & put it in a file
				#sys.exit("OUT")

 #  time.sleep(3600)
