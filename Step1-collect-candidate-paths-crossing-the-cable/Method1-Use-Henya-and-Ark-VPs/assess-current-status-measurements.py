from datetime import datetime
import time
import glob, time, os, sys


while 1:

   folders = glob.glob('Graph3/*')

   for elmt in folders:
	list_pairs = glob.glob(elmt + '/list*')
	print list_pairs

	for file in list_pairs:
		with open(file, 'r') as fh:
			for line in fh:
				print line
				tab1 = line.split(';')
				tab = tab1[-1].split('<==>')
				source = tab[0].split('__')
				dest =  tab[1].strip().split('__')

				## Run it
				## Detailed_From_South_America_after_SACS_towards_MZ_verified.txt; scl-cl__200.27.115.62__AS27678<==>196.10.148.169__196.10.148.0/24__AS37697

				print source[0], dest[0]
				command = "python vela-api.py --key 374bcf659bfcfec092b71c0736c5e5fc trace " + source[0] + ' ' + dest[0] + ' > output_run.txt'
				print command
				os.system(command)
				time.sleep(3)
				value = 0
				with open('output_run.txt', 'r') as fgh:
					for elmt1 in fgh:
						print elmt
						if 'result ID:' in elmt1:
							value = int(elmt1[elmt1.find(':')+1:])
							print value

				nowval = datetime.now()
				timestampval = time.time()
				## Get the results
				#if value != 0:
				#	command2 = "python vela-api.py --key 374bcf659bfcfec092b71c0736c5e5fc get " + str(value) + " > result.json" 
				#	os.system(command2)
                                #	time.sleep(3)

				with open(elmt + '/IDs_meas_' + tab1[0], 'a') as fk:
					fk.write('%s; %s; %s; %s; %s\n' %(timestampval, nowval, '--'.join(source), '--'.join(dest), value))

				## Transform & put it in a file
				#sys.exit("OUT")

   time.sleep(3600)
