## This script will run traceroutes with the vela API between Ark probes in the countries linked by the cable.
from datetime import datetime
from pprint import pprint
import os, time, sys


def get_list_probes(file):
    ## reads the list of probes in the file and appends them to a python list
    List_probes = []
    with open(file, 'r') as fg:
        for line in fg:
            List_probes.append(line.strip())
    return List_probes


def extract_set_probes_on_both_sides_of_link (Ark_probes, Countries_linked):
    ## identifies the probes whose names contain the country codes of the countries interconnected by the studied cable
    Group_probes = {}
    for probe in Ark_probes:
        for CC in Countries_linked:
            if CC not in Group_probes:
                Group_probes[CC] = []
            if '-'+ CC.lower() in probe:
                Group_probes[CC].append(probe)
    return Group_probes


def run_command(command):
    print('\n', command)
    os.system(command)
    time.sleep(3)



## These countries can be changed depending on the cable under study.
Countries_linked = ['BR', 'CA']
probe_file_exist = 0

if probe_file_exist:
    ## This file location can be modified by the user in case he wants to input another file.
    file_list_probes = "../../Datastore/list_probes.txt"
    Ark_probes = get_list_probes(file_list_probes)
    print(Ark_probes, len(Ark_probes), '\n')

    Probes_on_both_sides_of_cable = extract_set_probes_on_both_sides_of_link (Ark_probes, Countries_linked)
    pprint(Probes_on_both_sides_of_cable)

else:
    ## Use Vela API
    command = "/usr/local/bin/python tool-for-vela-api-usage.py --key 374bcf659bfcfec092b71c0736c5e5fc mons " + ' > list_probes.txt'
    run_command(command)


command = "/usr/local/bin/python tool-for-vela-api-usage.py --key 374bcf659bfcfec092b71c0736c5e5fc trace " + Probes_on_both_sides_of_cable[Countries_linked[0]][0] + ' ' + '8.8.8.8' + ' > output_run.txt'
os.system(command)
time.sleep(3)


if 0:
    value = 0
    with open('output_run.txt', 'r') as fgh:
        for elmt1 in fgh:
            print(elmt)
            if 'result ID:' in elmt1:
                value = int(elmt1[elmt1.find(':')+1:])
                print(value)

    nowval = datetime.now()
    timestampval = time.time()

    ## Get the results
    #if value != 0:
    #    command2 = "python vela-api.py --key 374bcf659bfcfec092b71c0736c5e5fc get " + str(value) + " > result.json"
    #    os.system(command2)
    #    time.sleep(3)

    #with open('IDs_meas_' + tab1[0], 'a') as fk:
    #    fk.write('%s; %s; %s; %s; %s\n' %(timestampval, nowval, '--'.join(source), '--'.join(dest), value))













