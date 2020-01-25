## Instructions: 2nd script to run for BGP data analysis (#Python)
## Objective:
## This script computes the Average AS path length distribution
## between the detected consistent AS pair before and after the
## studied cable launch.


from collections import Counter
from pprint import pprint
import math, sys, time

## This function determines the most common elmts X in a list
## count their number of occurences and rank the elmts X by
## decreasing order of those numbers.
## We intend to use it to compute the average AS path distribution
## for all consistent AS pair
def List_Most_Common(lst):
    data = Counter(lst)
    return data.most_common()


# Initializations
start_time = time.clock()
Result_folder = 'Results_set_1st_round'
Cable_operating_AS = '37468'
List_consistent_pairs = set([])
List_IP_paths_lengths_before = []
List_IP_paths_lengths_after = []
Dict_ASpath_length_per_pair_befor = {}
Dict_ASpath_length_per_pair_after = {}

    
## Read the set of consistent AS pairs from the corresponding file in the Result_folder
with open (Result_folder + '/Consistent_AS_pairs_transiting_cable_operating_AS.txt', 'r') as fg:
    for line in fg:
        List_consistent_pairs.add(line.strip())
    print ('Number of consistent pairs  = ', len(List_consistent_pairs))


with open (Result_folder + '/Paths_after_launch_via_Operating_AS.txt', 'r') as fh:
    for line in fh:
        line = line.strip()
        tab = line.split(' ')
        if len(tab) >= 2:
            ASpath = tab[2].split('|')
            if tab[0] not in Dict_ASpath_length_per_pair_after:
                Dict_ASpath_length_per_pair_after[tab[0]] = []
                Dict_ASpath_length_per_pair_after[tab[0]].append(len(ASpath))

with open (Result_folder + '/Paths_before_launch_via_Operating_AS.txt', 'r') as fh:
    for line in fh:
        line = line.strip()
        tab = line.split(' ')
        if len(tab) >= 2:
            ASpath = tab[2].split('|')
            if tab[0] not in Dict_ASpath_length_per_pair_befor:
                Dict_ASpath_length_per_pair_befor[tab[0]] = []
                Dict_ASpath_length_per_pair_befor[tab[0]].append(len(ASpath))


#### compute the Average path length per pair:

# More Initializations
Av_path_length_befor = {}
Av_path_length_after = {}
List_values_after = []
List_values_befor = []


## Compute the Average AS path length distribution between each detected consistent
## AS pair before the cable launch
for key in Dict_ASpath_length_per_pair_after:
    if key in  Dict_ASpath_length_per_pair_befor:
        if key not in Av_path_length_after:
            Av_path_length_after[key]= 0
        Av_path_length_after[key] = (1.0*sum(Dict_ASpath_length_per_pair_after[key])) /len(Dict_ASpath_length_per_pair_after[key])
        List_values_after.append(math.ceil(Av_path_length_after[key]))


## Compute the Average AS path length distribution between each detected consistent
## AS pair after the cable launch
for key in Dict_ASpath_length_per_pair_befor:
    if key in  Dict_ASpath_length_per_pair_after:
        if key not in Av_path_length_befor:
            Av_path_length_befor[key]= 0
        Av_path_length_befor[key] = (1.0* sum(Dict_ASpath_length_per_pair_befor[key])) /len(Dict_ASpath_length_per_pair_befor[key])
        List_values_befor.append(math.ceil(Av_path_length_befor[key]))


## Compute AS path length distribution.
print('AS path length distribution')
print 'List_IP_paths_lengths_before = ', List_Most_Common(List_values_befor), len(List_values_befor)
print 'List_IP_paths_lengths_after = ', List_Most_Common(List_values_after), len(List_values_after)


## Store all the values of the average path length distribution in a .txt file for post computation with Matlab.
## Output: Average AS_paths lengths for paths between consistent AS pairs transiting Operating AS before launch
with open ('Average_AS_paths_length_before_launch.txt', 'a') as fgh2:
    for elmt in List_values_befor:
        fgh2.write('%s\n' %(elmt))

with open ('Average_AS_paths_length_after_launch.txt', 'a') as fgh1:
    for elmt in List_values_after:
        fgh1.write('%s\n' %(elmt))

