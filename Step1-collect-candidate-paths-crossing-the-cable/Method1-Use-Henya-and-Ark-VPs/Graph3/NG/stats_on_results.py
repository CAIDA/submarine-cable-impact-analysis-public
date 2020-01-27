from __future__ import division
import glob


list_files = glob.glob('Outputs*')

print list_files




for file in list_files:
	with open(file, 'r') as fj:
		via_SACS =  0

		List_pairs_via_SACS = []
		List_pairs_measured = []

		List_IP_pairs_measured = []
		Number_of_meas = []

		via_AOC = []

		for elmt in fj:
			if '--' in elmt and ';' in elmt:
				tab = elmt.split('; ')
				tab1 =  tab[3].split('--')
				del(tab1[0])
				pair = str(tab[2] + '<==>' + '--'.join(tab1)).strip()
			
			if 'src' in elmt and 'dst' in elmt:
				if pair not in  List_pairs_measured:
					List_pairs_measured.append(pair)
				
				IPpair = str(elmt).strip()
				if IPpair not in List_IP_pairs_measured:
					List_IP_pairs_measured.append(IPpair)			
				Number_of_meas.append(IPpair)

			if 'AS37468' in elmt or ' 37468 ' in elmt:
				if pair not in via_AOC:
					via_AOC.append(pair)

			if 'SACS' in elmt:
				 via_SACS +=1
				 if pair not in List_pairs_via_SACS:
					 List_pairs_via_SACS.append(pair)




	print file, via_SACS 
	print 'List_pairs_via_SACS = ', len(List_pairs_via_SACS) #, List_pairs_via_SACS
	print 'List_pairs_measured = ', len(List_pairs_measured) #, List_pairs_measured
	print 100*len(List_pairs_via_SACS)/len(List_pairs_measured)
	print 'Via_AOC = ', 100*len(via_AOC)/len(List_pairs_measured) 
	print
	print 'List_IP_pairs_measured = ', len(List_IP_pairs_measured)
	print 'Number of measurements = ', len(Number_of_meas)
	print len(Number_of_meas)/len(List_IP_pairs_measured)
	print
