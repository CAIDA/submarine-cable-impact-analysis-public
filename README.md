Note: This repository is still being updated. 

PAM Paper: Unintended consequences: Effects of submarine cable deployment on Internet routing (https://www.caida.org/publications/papers/2020/unintended_consequences/)

# submarine-cable-impact-analysis

Our methodology can be divided into 4 steps. Each of them corresponds to the first 4 directories of this repository:  
* Step1-collect-candidate-paths-crossing-the-cable
* Step2-identify-router-IPs-on-both-sides
* Step3-search-for-comparable-historical-traceroutes
* Step4-annotate-collected-paths

We added in Step5-data-analysis the scripts used for data analysis

## Python packages to install for running the scripts smoothly
E.g. pip install --target=/usr/local/bin pyasn
* Wandio
* urllib2 (Python2) or urllib (Python3)
* IPy (https://pypi.org/project/IPy/)
* pyasn (https://pypi.org/project/pyasn/)
* dnspython (https://pypi.org/project/dnspython/)
* docopt (https://pypi.org/project/docopt/) 
* pycountry-convert (https://pypi.org/project/pycountry-convert/)
 
## Brief description of the folders' content   
### Step 1: Collect candidate IP paths that could have crossed the cable.
This folder contains the scripts for 2 possible ways for achieving this goal (Method1-Use-Henya-and-Ark-VPs and Method2-Use-RIPE-Atlas-VPs). The first method can be used for Ark VPs, while the second can be used for RIPE Atlas probe. 

### Step 2: Identify router IP interfaces on both sides of the cable.
To identify the router IP interfaces, you can run the script 1_identify_router_IPs_from_ITDK_data_v2.py. The links IPs are listed in Final_list_IPs_RA.txt, and Final_list_IPs_RB.txt

### Step 3: Search for comparable historical traceroutes.



### Step 4: Annotate collected paths.


### Step 5: Data analysis.
You can use the script 1_Finding_Consistent_AS_pairs_transiting_cable_operating_AS.py to find consistent AS pairs transiting the AS operating the cable, and 2_Computing_lengths_AS_paths_between_consistent_AS_pairs.py to compute the length of AS paths between the same AS, destination prefixes pre & post SACS.

## Access to the data
