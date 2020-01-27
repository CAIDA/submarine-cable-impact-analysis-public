import sys

pairs_suboptimalities = []

if 0:
   with open ('Outputs_meas_Detailed_From_North_America_after_SACS_towards_AO_verified.txt', 'r') as fg:
	num_eu =  0
        via_sacs = 0
	added =0
	new_rtt = 0
	for line in fg:
		print line

		if added == 1 and ';' not in line and ('.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line):
			values = line.split(' ')
                        if len(values) >3:
                                print values[3][:-2]
                                new_rtt = float(values[3][:-2])
				#print 'CHECKS',  new_rtt, old_rtt, val
			  	if new_rtt - old_rtt > 30:
					num_eu +=1
					print 'adding an increment '
				added =0	

		if ';' in line:
			## Update suboptimality info
			if num_eu >0 and via_sacs >0:
				if current_pair not in pairs_suboptimalities:
					pairs_suboptimalities.append(current_pair)
			## Continue
			tab = line.split(';')
			current_pair = str(tab[2]).strip() + '; ' + str(tab[3]).strip()

			print current_pair
			num_eu = 0
			via_sacs = 0

		else:
			values = line.split(' ')
			if len(values) >3:
				print values[3][:-2]
				new_rtt = float(values[3][:-2])
				
		## We would have suboptimality if the packets go through EU and SACS or SACS and EU
		if '.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line:
			#num_eu +=1
			#print 'CHECKING = ', new_rtt, old_rtt
			if new_rtt - old_rtt > 30:
                              num_eu +=1

			added +=1
			val = line

		if 'VIA_SACS' in line:
			via_sacs +=1	

		old_rtt = new_rtt

   print 'North America => AO =', pairs_suboptimalities
   sys.exit('out')







if 0:
    with open ('Outputs_meas_Detailed_From_Africa_after_SACS_towards_AO_verified.txt', 'r') as fg:
        num_eu =  0
        via_sacs = 0
        added =0
        new_rtt = 0
        for line in fg:
                print line

                if added == 1 and ';' not in line and ('.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line):
                        values = line.split(' ')
                        if len(values) >3:
                                print values[3][:-2]
                                new_rtt = float(values[3][:-2])
                                #print 'CHECKS',  new_rtt, old_rtt, val
                                if new_rtt - old_rtt > 30:
                                        num_eu +=1
                                        print 'adding an increment '
                                added =0        

                if ';' in line:
                        ## Update suboptimality info
                        if num_eu >0 or via_sacs >0:
                                if current_pair not in pairs_suboptimalities:
                                        pairs_suboptimalities.append(current_pair)
                        ## Continue
                        tab = line.split(';')
                        current_pair = str(tab[2]).strip() + '; ' + str(tab[3]).strip()

                        print current_pair
                        num_eu = 0
                        via_sacs = 0

                else:
                        values = line.split(' ')
                        if len(values) >3:
                                print values[3][:-2]
                                new_rtt = float(values[3][:-2])
                                
                ## We would have suboptimality if the packets go through EU and SACS or SACS and EU
                if '.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line:
                        #num_eu +=1
                        #print 'CHECKING = ', new_rtt, old_rtt
                        if new_rtt - old_rtt > 30:
                              num_eu +=1

                        added +=1
                        val = line

                if 'VIA_SACS' in line:
                        via_sacs +=1    

                old_rtt = new_rtt

    print 'Africa => AO =', len(pairs_suboptimalities), pairs_suboptimalities



if 1: 
    with open ('Outputs_meas_Detailed_From_Asia_after_SACS_towards_AO_verified.txt', 'r') as fg:
        num_eu =  0
        via_sacs = 0
        added =0
        new_rtt = 0
        for line in fg:
                print line

                if added == 1 and ';' not in line and ('.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line):
                        values = line.split(' ')
                        if len(values) >3:
                                print values[3][:-2]
                                new_rtt = float(values[3][:-2])
                                #print 'CHECKS',  new_rtt, old_rtt, val
                                if new_rtt - old_rtt > 30:
                                        num_eu +=1
                                        print 'adding an increment '
                                added =0        

                if ';' in line:
                        ## Update suboptimality info
                        if num_eu >0 and via_sacs >0:
                                if current_pair not in pairs_suboptimalities:
                                        pairs_suboptimalities.append(current_pair)
                        ## Continue
                        tab = line.split(';')
                        current_pair = str(tab[2]).strip() + '; ' + str(tab[3]).strip()

                        print current_pair
                        num_eu = 0
                        via_sacs = 0

                else:
                        values = line.split(' ')
                        if len(values) >3:
                                print values[3][:-2]
                                new_rtt = float(values[3][:-2])
                                
                ## We would have suboptimality if the packets go through EU and SACS or SACS and EU
                if '.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line:
                        #num_eu +=1
                        #print 'CHECKING = ', new_rtt, old_rtt
                        if new_rtt - old_rtt > 30:
                              num_eu +=1

                        added +=1
                        val = line

                if 'VIA_SACS' in line:
                        via_sacs +=1    

                old_rtt = new_rtt

    print 'Asia => AO =', len(pairs_suboptimalities), pairs_suboptimalities




if 1: 
    with open ('Outputs_meas_Detailed_From_Europe_after_SACS_towards_AO_verified.txt', 'r') as fg:
        num_eu =  0
        via_sacs = 0
        added =0
        new_rtt = 0
        for line in fg:
                print line

                if ';' in line:
                        ## Update suboptimality info
                        if via_sacs >0:
                                if current_pair not in pairs_suboptimalities:
                                        pairs_suboptimalities.append(current_pair)
                        ## Continue
                        tab = line.split(';')
                        current_pair = str(tab[2]).strip() + '; ' + str(tab[3]).strip()

                        print current_pair
                        num_eu = 0
                        via_sacs = 0
                else:
                        values = line.split(' ')
                        if len(values) >3:
                                print values[3][:-2]
                                new_rtt = float(values[3][:-2])

                if 'VIA_SACS' in line:
                        via_sacs +=1    

                old_rtt = new_rtt

    print 'Europe => AO =', len(pairs_suboptimalities), pairs_suboptimalities


