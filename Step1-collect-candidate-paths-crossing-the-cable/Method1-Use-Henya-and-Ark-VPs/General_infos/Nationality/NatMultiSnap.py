import pandas as pd
import os
import glob
import numpy as np

path='/project/comcast-ping/stabledist/mapkit/code/Nationality'
os.chdir(path)



snapshots_list = [
    '20180101',
    '20180201',
    '20180301',
    '20181201',
    '20180901',
    '20180601',
    '20171201',
    '20170901',
    '20170601',
    '20170301',
    '20161201',
    '20160901',
    '20160601',
    '20160301',
    '20151201',
    '20150901',
    '20150601',
    '20150301',
    '20141201',
    '20140901',
    '20140601',
    '20140301',
    '20131201',
    '20130901',
    '20130601',
    '20130301',
    '20121201',
    '20120901',
    '20120601',
    '20120301',
    '20111201',
    '20110901',
    '20110601',
    '20110301',
    '20101201',
    '20100901',
    '20100601',
    '20100301']

#snapshots_list = [
#    '20180101',
#    '20180201',
#    '20180301']





#/project/mapkit/agamerog/country_asn_analysis/geolocation_bgp/pfxgeo


for snapshot in snapshots_list:
    #P2C_df=pd.read_csv('/project/mapkit/agamerog/country_asn_analysis/as-rank-ribs/%s.as-rel.txt'%snapshot,comment='#',header=None,sep='|')
    print 'rawData/%s.as-rel.txt'%snapshot
    #if len(glob.glob('rawData/%s.as-rel.txt'%snapshot))==0 or len(glob.glob('/project/mapkit/agamerog/country_asn_analysis/geolocation_bgp/pfxgeo/asn-to-country.%s-%s-%s'%(snapshot[0:4],snapshot[4:6],snapshot[6:8])))==0:
    if len(glob.glob('rawData/%s.as-rel.txt'%snapshot))==0 or len(glob.glob('rawData/asn-to-country.%s-%s-%s'%(snapshot[0:4],snapshot[4:6],snapshot[6:8])))==0:
        print "The P2C file for the snapshot (%s) is not available"%snapshot
    else:
        P2C_df=pd.read_csv('rawData/%s.as-rel.txt'%snapshot,comment='#',header=None,sep='|')
        P2C_df.columns=['provider','customer','type']
        #geoloc_df=pd.read_csv('/project/mapkit/agamerog/country_asn_analysis/geolocation_bgp/pfxgeo/asn-to-country.%s-%s-%s'%(snapshot[0:4],snapshot[4:6],snapshot[6:8]),header='infer',sep='|')
        geoloc_df=pd.read_csv('rawData/asn-to-country.%s-%s-%s'%(snapshot[0:4],snapshot[4:6],snapshot[6:8]),header='infer',sep='|')
        cc2rir_df=pd.read_csv('/project/comcast-ping/stabledist/mapkit/code/state-owned_ASes/extraFiles/cc2rir.csv',header='infer')
        
        ASes_set_a=np.unique(np.append(P2C_df['provider'].values,P2C_df['customer'].values))
        
        StubASes_v=[]
        NONStubASes_v=[]
        for ASN in ASes_set_a:
            if P2C_df.loc[(P2C_df['provider']==ASN) & (P2C_df['type']==-1)]['customer'].values.size==0:
                StubASes_v.append(ASN)
            #PseudoSTUBS: ASes which have customers but none of those customers appear on BG
            elif geoloc_df.loc[geoloc_df['#asn'].isin(P2C_df.loc[(P2C_df['provider']==ASN) & (P2C_df['type']==-1)]['customer'].values) & (~geoloc_df['#asn'].isnull())].drop_duplicates('#asn')['#asn'].values.size==0:
                StubASes_v.append(ASN)
            else:
                NONStubASes_v.append(ASN)
                
                
        # Geolocating Stub ASes
        
        geolocSTUBS_df=geoloc_df.loc[geoloc_df['#asn'].isin(StubASes_v)]            
        I=geolocSTUBS_df.groupby('#asn')['ip-pct'].transform(max) == geolocSTUBS_df['ip-pct']
        STUBSmainprecense_df=geolocSTUBS_df.ix[I]
        
        Nationality_df=STUBSmainprecense_df[['#asn','country-code']]
        Nationality_df.columns=['ASN','cc']
        # A VERY FEW (221 OUT OF 37500) are evenly splitted in more than one country
        #Nationality_df.shape
        Nationality_df=Nationality_df.drop_duplicates('ASN')
        #Nationality_df.shape
        
        # Deciles of ip-pct of Stub ASes. They're likely to be geolocated in just one country
        np.percentile(STUBSmainprecense_df['ip-pct'].values,range(0,101,10))
        
        # WARNING!!
        # Some customers are no present in BG file!!!
        
        # Geolocating NON Stub ASes
        
        S=[]
        R=0
        while len(NONStubASes_v)>0 and R<150:
            NewEntries_v=[]
            i=0
            for ASN in NONStubASes_v:
            #for ASN in (3356,):
                # Attemp to classify if Transit was not already classified
                if ASN not in Nationality_df['ASN'].values:
                    
                    # This is twofold to prevent the lack of some customers in BG file
                    rawCustomers_a=P2C_df.loc[(P2C_df['provider']==ASN) & (P2C_df['type']==-1)]['customer'].values
                    customers_a=geoloc_df.loc[geoloc_df['#asn'].isin(rawCustomers_a) & (~geoloc_df['#asn'].isnull())].drop_duplicates('#asn')['#asn'].values
                    
                    # if all customers are already localize, then proceed to classify the Transit
                    if customers_a.size==Nationality_df[(Nationality_df['ASN'].isin(customers_a)) & (~Nationality_df['ASN'].isnull())]['ASN'].size and customers_a.size>0:
                        #print ASN
                        #break
                        # There are some entries where CC is NaN. Those have to be removed
                        CustomersNationality_a=Nationality_df[(Nationality_df['ASN'].isin(customers_a)) &(~Nationality_df['ASN'].isnull())].groupby(['cc']).count().reset_index()[['ASN','cc']].sort_values('ASN',ascending=False).values
                        if CustomersNationality_a.size>0:
                            if CustomersNationality_a[0][0]>(customers_a.size/2):
                                #print R,ASN,CustomersNationality_a[0][1]
                                NewEntries_v.append((ASN,CustomersNationality_a[0][1]))
                                NONStubASes_v.pop(i)
                            else:
                                NewEntries_v.append((ASN,'XX'))
                                NONStubASes_v.pop(i)
                                #print R,ASN,'XX'
                        else:
                            NewEntries_v.append((ASN,'??'))
                            NONStubASes_v.pop(i)
                            #print "All customers where found as geolocated in NaN"
                    else:
                        #print '%s,%s Not ready'%(R,ASN)
                        pass
                i+=1
            
            NewEntries_df=pd.DataFrame(list(NewEntries_v),columns=['ASN','cc'])
            Nationality_df=Nationality_df.append(NewEntries_df)
            S.append((R,len(NONStubASes_v)))
            R+=1
            ##
            ##
            ##
            # CONTIUNE--> SAVE
            Nationality_df.to_csv('%s.csv'%snapshot,header=True,index=False)
