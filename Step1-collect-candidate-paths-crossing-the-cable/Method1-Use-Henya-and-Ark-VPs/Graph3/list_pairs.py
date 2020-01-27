import glob, os, sys

direct = '/Users/Roderick/Documents/0_CAIDA_Work/Papers/1_SACS/4_Preparing_resubmission/2_crosscheck_IP_paths_go_via_SACS/Data_After_call_with_AOC/launch_meas_Vela_API/Graph3/'
folders = glob.glob(direct + '/*')

print(folders)

for elmt in folders:
    final_folder = glob.glob(elmt + '/After/Detailed_*')
    
    if len(final_folder) > 1:
        for file in final_folder:
            List_unik_pairs = []
            tab = file.split('/')
            print(final_folder, tab[-1])

            with open(elmt + '/list_pairs_' + tab[-3], 'a') as fg:
                
                with open(file, 'r') as fh:
                    for line in fh:
                        info1 = line.split('<==>')
                        info = info1[1].split('\t')

                        var = info[3] + '__' + info[4] + '__' + info[5] + '<==>' + info[6] + '__' + info[7] + '__' + info[8]
                        #print(var)

                        if var not in List_unik_pairs:
                            List_unik_pairs.append(var)

                for line in List_unik_pairs:
                    fg.write('%s; %s\n'%(tab[-1], line))
