from bz2 import BZ2File as bzopen

## Find all IPs that are aliases with both sides of the SACS link in January 2019
ITDK_folders = ['/data/topology/ITDK/ITDK-2019-01/']


### Add list of potential IPs here
#Brazil
Potential_IPs_RB = ['170.238.233.58', '170.238.233.56', '170.238.232.66', '170.238.232.82', '170.238.232.145']
#Angola
Potential_IPs_RA = ['170.238.232.146', '197.149.149.162', '170.238.232.150', '170.238.232.155']


for ITDK_folder in ITDK_folders:
    # reading a bz2 archive
    with bzopen(ITDK_folder + "kapar-midar-iff.nodes.bz2", "r") as bzfin:
        """ Handle lines here """
        lines_RB = []
        List_IPs_RB = []
        
        lines_RA = []
        List_IPs_RA = []
        
        for i, line in enumerate(bzfin):
            """ look for nodes containing potential_IPs_RB """
            for link_IP in Potential_IPs_RB:
                if link_IP in line and line.rstrip() not in lines_RB:
                    lines_RB.append(line.rstrip())
        
            """ look for nodes containing potential_IPs_RA """
            for link_IP in Potential_IPs_RA:
                if link_IP in line and line.rstrip() not in lines_RA:
                    lines_RA.append(line.rstrip())

        with open ('corresponding_nodes_and_IP_aliases_itdk_RAngola.txt', 'w') as fj1:
            fj1.write('\n%s \n' %(ITDK_folder + "kapar-midar-iff.nodes.bz2"))
            for data in lines_RA:
                fj1.write('%s\n' %(''.join(data)))
                if data != "":
                    tab = data.split(' ')
                    for kk in tab:
                        if 'node' not in kk and 'N' not in kk and kk != '':
                            List_IPs_RA.append(kk)

        with open ('corresponding_nodes_and_IP_aliases_itdk_RBrasil.txt', 'w') as fj2:
            fj2.write('\n%s \n' %(ITDK_folder + "kapar-midar-iff.nodes.bz2"))
            for data in lines_RB:
                fj2.write('%s\n' %(''.join(data)))
                if data != "":
                    tab = data.split(' ')
                    for kk in tab:
                        if 'node' not in kk and 'N' not in kk and kk != '':
                            List_IPs_RB.append(kk)

        print ('List_IPs_RB = ', list(set(List_IPs_RB)))
        print ('List_IPs_RA = ', list(set(List_IPs_RA)))

        Final_list_IPs_RB = list(set(List_IPs_RB)) + Potential_IPs_RB
        Final_list_IPs_RA = list(set(List_IPs_RA)) + Potential_IPs_RA

        # Final list Aliases
        with open ('Final_list_IPs_RB.txt', 'w') as Rb:
            for IP in Final_list_IPs_RB:
                Rb.write('\n%s' %(IP))
                    
        with open ('Final_list_IPs_RA.txt', 'w') as Ra:
            for IP in Final_list_IPs_RA:
                Ra.write('\n%s' %(IP))
 
    print ('Done')
