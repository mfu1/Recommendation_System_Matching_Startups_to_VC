import pandas
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt 
import numpy as np
from datetime import datetime, date, time
import operator
import ast
#df.shape[0] instead, which will always correctly tell you the number of rows
#infile=pandas.read_csv("investments.csv",dtype={'company_name': str})
#
#uni_2014_relation.csv
#print df.shape


infile=pandas.read_csv("investments.csv",dtype={'company_name': str})
df =  infile.loc[:,['company_name','investor_name','company_country_code','investor_country_code','funded_at']]

df['invest_index'] = range(1, df.shape[0]  + 1)
dicOrgEIN= df.set_index('invest_index').T.to_dict()

#print dicOrgEIN[1]

investorLs=[]
investedLs=[]
relationInv=[]
testRelation=[]
#count1=0
for n in range(1, df.shape[0]  + 1):
#if dicOrgEIN[n]['company_country_code'] == 'USA' and dicOrgEIN[n]['investor_country_code'] == 'USA' :
    dta = datetime.strptime(dicOrgEIN[n]['funded_at'], "%Y-%m-%d")
    
   # print int(dta.year) == 2014
    if int(dta.year) == 2014:
     
        investorLs.append(dicOrgEIN[n]['investor_name'])
        investedLs.append(dicOrgEIN[n]['company_name'])
        
#        #print count1
#       # dta = datetime.strptime(dicOrgEIN[n]['funded_at'], "%Y-%m-%d")
        relationInv.append((dicOrgEIN[n]['investor_name'],dicOrgEIN[n]['company_name']))
#        
#    if int(dta.year) == 2015:
#        testRelation.append((dicOrgEIN[n]['company_name'],dicOrgEIN[n]['investor_name']))
#        
print '****************'
investorSet=set(investorLs)
#print len(investorSet)
investedSet=set(investedLs)

investorSet2 = investorSet.difference(investedSet)
investedSet2 = investedSet.difference(investorSet)
#print len(investorSet2)
print len(investedSet2)
#print '**********'
relationInv2=[]
for n in relationInv:
    if n[0] in investorSet2:
        if n[1] in investedSet2:
            relationInv2.append(n)
print len(relationInv)
print len(relationInv2)



B=nx.Graph()

B.add_nodes_from(investorSet2,investor = 1 )
B.add_nodes_from(investedSet2,investor = 0 )
B.add_edges_from(relationInv2)

giant = max(nx.connected_component_subgraphs(B), key=len)

print nx.number_of_nodes (B)
print nx.number_of_nodes (giant) #15367


######################################################
#Generate the Prediction Csv
######################################################
with open('Predict2015_3','a') as f:
        f.write('company_name\tinvestor_name\n')
countTotal=0
for n in investedSet2:
    count=0
   
    lsall=[]
    ls1=B.neighbors(n)
    #print len(ls1)
    lsall=ls1[:]
    for n2 in ls1:
        ls2=B.neighbors(n2)
        lsall+=ls2
        count +=1
        for n3 in ls2:
            ls3=B.neighbors(n3)
  
            lsall+=ls3
            count +=1
  
    s = B.subgraph(lsall)
    a = nx.pagerank(s)
    sorted_a = sorted(a.items(), key=operator.itemgetter(1), reverse = True)
    #print sorted_a
    resultLs=[]
    count2=0
    flag=True
    for sort_name in sorted_a:
        if sort_name[0] in investorSet2:
            resultLs.append(sort_name[0])
            count2+=1
        if len(resultLs)>=3:
            with open('Predict2015_3','a') as f:
                f.write('{}\t{}\n'.format(n,resultLs))
                countTotal+=1
                flag=False
                break
                print countTotal
            
    if flag:
        with open('Predict2015_3','a') as f:
            f.write('{}\t{}\n'.format(n,resultLs))
            #print resultLs
            countTotal+=1
            print countTotal
             
             #continue
   
    

########################Evalution##############################

    
test_file=pandas.read_csv("uni_2015_relation.csv")
df2 =  test_file.loc[:,['company_name','investor_name']]
test_dic = {}
for n,row in df2.iterrows():
    if row[0] in test_dic:
        test_dic[row[0]].append(row[1])
    else:
        test_dic[row[0]]=[row[1]]


old_2014 = {}
test_file=pandas.read_csv("uni_2014_relation.csv")
df2 =  test_file.loc[:,['company_name','investor_name']]
for n,row in df2.iterrows():
    if row[0] in old_2014:
        old_2014[row[0]].append(row[1])
    else:
        old_2014[row[0]]=[row[1]]
  

result_dic={}
with open('Predict2015_3','r') as f:
    for n in f.readlines()[1:]:
        result_dic[n.split('\t')[0]]=n.strip().split('\t')[1]
        print len(result_dic.keys())

for n in result_dic:
    try:
        result_dic[n]=ast.literal_eval(result_dic[n])
    except:
        pass


eval_dic={}    
for n in result_dic:
    
    if n in test_dic:
        print n
        #n='Loanbase'
        count=0
        #print 
        for investor in  result_dic[n]:
            #print investor
            #if investor in test_dic[n]:
            if investor in test_dic[n] and investor not in old_2014[n]:
               # print investor
                count+=1
        print count
        try:
        
            score=float(count)/float(len(result_dic[n]))
            eval_dic[n]=score
        except:
            pass
        
with open('evlautaion_2015_3_no_old','w') as f:
    for n in eval_dic.keys():
        f.write('{}\t{}\n'.format(n,eval_dic[n]))
    
        
#    
#
#giant = max(nx.connected_component_subgraphs(B), key=len)
##len(giant)
#gaintNode=set(giant.nodes())
#

##
###print nx.degree_centrality(g)
###print nx.closeness_centrality(g)
###print nx.betweenness_centrality(g)
###
##
