## Instructions: 1st script to run for BGP data analysis
## Objective:
## This script compares all paths without loops going via the AS operating the cable
## (in this case AS37468) during the first 5 days of the month before the launch and
## that after the launch. It then identifies the list of AS couples that are found in
## both sets, which are termed consistent AS pairs.


import wandio, os, sys, time

# Initializations
limit = 0
start_time = time.clock()
Result_folder = 'Results_set_1st_round'
Cable_operating_AS = '37468'
List_couples_after_cable_launch = set([])

## Create Result_set folder
try:
    os.mkdir(Result_folder, 0755)
except:
    pass

## When running in the CAIDA environment
path_to_as_rank_ribs = '/data/external/as-rank-ribs/'
before_file = path_to_as_rank_ribs + '20180801/20180801.all-paths.bz2'
after_file = path_to_as_rank_ribs + '20181001/20181001.all-paths.bz2'

## When running locally
#path_to_as_rank_ribs = '/Data/bgp-data/'
#before_file = path_to_as_rank_ribs + '08_01-05/20180801.all-paths.bz2'
#after_file = path_to_as_rank_ribs + '10_01-05/20181001.all-paths.bz2'

## We traverse the list of AS paths after cable launch and store in
## 'Paths_after_launch_via_Operating_AS.txt' only AS paths containing
## the Operating AS
with open(Result_folder + '/Paths_after_launch_via_Operating_AS.txt', 'a') as fh1:
    print 'Step1: After File'
    with wandio.open(after_file, 'r') as fg:
        for line in fg:
            #print ("line =",  line.strip())
            line = line.strip()
            tab = line.split(' ')
            AS_path = tab[1].split('|')
            AS_pair = AS_path[0]+ '-' +AS_path[-1]
            #print('AS_pair = ', AS_pair)
            #print('AS_path = ',  AS_path, "\n")
            
            if Cable_operating_AS in AS_path :
                List_couples_after_cable_launch.add(AS_pair)
                fh1.write('%s %s\n' %(AS_pair, line))

## For test purposes
#            limit += 1
#            if limit == 10000000:
#            	break


end_time = time.clock()
print ("The part 1 of the script was executed in =", end_time - start_time, "seconds", "\n")


# Initializations
limit = 0

## We traverse the list of AS paths before cable launch and store in
## 'Paths_before_launch_via_Operating_AS.txt' only AS paths containing
## the Operating AS. We also build the set of consistent AS pairs which
## are found befor and after the cable launch.
print 'Step2: Before File'
with open(Result_folder + '/Paths_before_launch_via_Operating_AS.txt', 'a') as fh11:
    with open(Result_folder + '/Consistent_AS_pairs_transiting_cable_operating_AS.txt', 'a') as fh22:
        with wandio.open(before_file, 'r') as fg2:
            for line in fg2:
                #print ("line =",  line.strip())
                tab = line.split(' ')
                AS_path = tab[1].split('|')
                AS_pair = AS_path[0]+ '-' +AS_path[-1]
                
                if AS_pair in List_couples_after_cable_launch:
                    print ('found consistent AS pair', AS_pair)
                    fh11.write('%s %s\n' %(AS_pair, line))
                    fh22.write('%s\n' %(AS_pair))

## For test purposes
#                limit += 1
#                if limit == 10000000000:
#                    break

end_time = time.clock()
print ("The script was executed in = ", end_time - start_time, "seconds", "\n")

print ("The total number of consistent AS pairs is = ", len(List_couples_after_cable_launch))
