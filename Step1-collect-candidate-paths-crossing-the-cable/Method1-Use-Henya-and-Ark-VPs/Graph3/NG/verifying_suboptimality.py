import sys

pairs_suboptimalities = []

with open ('Outputs_meas_Detailed_From_North_America_after_SACS_towards_NG_verified.txt', 'r') as fg:
	num_eu =  0
        via_sacs = 0

	for line in fg:
		print line

		if ';' in line:
			## Update suboptimality info
			if num_eu >0 and via_sacs >0:
				pairs_suboptimalities.append(current_pair)

			## Continue
			tab = line.split(';')
			current_pair = str(tab[2]).strip() + '; ' + str(tab[3]).strip()

			print current_pair
			num_eu =  0
			via_sacs = 0


		## We would have suboptimality if the packets go through EU and SACS or SACS and EU
		if '.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line or '.cpt' in line:
			num_eu +=1

		if 'VIA_SACS' in line:
			via_sacs +=1	


print 'North_America => NG =', pairs_suboptimalities
#sys.exit('out')




pairs_suboptimalities = []
with open ('Outputs_meas_Detailed_From_Asia_after_SACS_towards_NG_verified.txt', 'r') as fg:
        num_eu =  0
        via_sacs = 0

        for line in fg:
                print line

                if ';' in line:
                        ## Update suboptimality info
                        if num_eu >0 and via_sacs >0:
                                pairs_suboptimalities+= current_pair

                        ## Continue
                        tab = line.split(';')
                        current_pair = str(tab[2]).strip() + '; ' + str(tab[3]).strip()

                        print current_pair
                        num_eu =  0
                        via_sacs = 0

		## We would have suboptimality if the packets go through EU and SACS

                if '.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line or '.cpt' in line:
                        num_eu +=1

                if 'VIA_SACS' in line:
                        via_sacs +=1    


print 'Asia => NG =', pairs_suboptimalities
#sys.exit('OUT')




pairs_suboptimalities = []
with open ('Outputs_meas_Detailed_From_Oceania_Australia_after_SACS_towards_NG_verified.txt', 'r') as fg:
        num_eu =  0
        via_sacs = 0

        for line in fg:
                print line

                if ';' in line:
                        ## Update suboptimality info
                        if num_eu >0 and via_sacs >0:
                                pairs_suboptimalities+= current_pair

                        ## Continue
                        tab = line.split(';')
                        current_pair = str(tab[2]).strip() + '; ' + str(tab[3]).strip()

                        print current_pair
                        num_eu =  0
                        via_sacs = 0

                ## We would have suboptimality if the packets go through EU and SACS

                if '.lis' in line or '.par' in line or '.fra.' in line or '.lon' in line or '.uk' in line or '.ldn' in line or '.cpt' in line:
                        num_eu +=1

                if 'VIA_SACS' in line:
                        via_sacs +=1    


print 'Oceania_Australia => NG =', pairs_suboptimalities
#sys.exit('OUT')





