import glob

#base = '/home/roderick/CAIDA_Work/17_IMC_traceroutes_data_parsing/8_Fine_tune_Ark_data_parsing/'
base = '/home/roderick/CAIDA_Work/20_launch_meas_with_Vela/General_infos/'
List_files = glob.glob(base + 'prefix_AS/*')

for file in List_files:
    filename = file.split('/')

    name = filename[-1].split('.')

    with open(base + '/data_files/' + filename[-1] + '.dat', 'w') as fh:
	
	fh.write('%s\n'%('; IP-ASN32-DAT file'))
	fh.write('%s\n'%('; Original file : ' + base + '/data_files/' + filename[-1] + '.dat'))
	fh.write('%s\n'%('; Converted on  : ' + name[0]))
	fh.write('%s\n'%('; CIDRs         : 60000'))
	fh.write('%s\n'%(';			'))

	print file

	with open(file, 'r') as fg:
		for line in fg:
			line = line.strip()
			print line

			if line != '' and '|' not in line:
                        	#print line
                                tab = line.split('\t')
	
				if '_' not in tab[2]:
                                        ASNs = []
                                        ASNs.append(tab[2])
                                else:   
                                        tab1 = tab[2].split('_')
                                        ASNs = []
                                        ASNs.append(int(tab1[0]))
                                        ASNs.append(int(tab1[1]))
		
				for ASN in ASNs: 
					fh.write('%s\t%s\n' %( tab[0] + '/' + tab[1], ASN ))						
