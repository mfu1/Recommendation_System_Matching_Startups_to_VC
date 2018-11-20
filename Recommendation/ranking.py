'''
Created on Sun Apr 16 2017

@author: Hui Liang
'''

############################################################################
# Clean Date and Parse into Dictionary 
############################################################################


import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite

from data import testing_company
from data import startup_dict2015
from data import startup_dict

df = pd.read_csv('650Project_Dataset_Cleaned_updated.csv', parse_dates = ['funded_at'], thousands=',')
df.drop('company_permalink', axis=1, inplace=True)
df.drop('investor_permalink', axis=1, inplace=True)
df.drop(df.columns[0], axis=1, inplace=True)

df2014 = df[(df['funded_at'] >= '2014-01-01') & (df['funded_at'] <= '2014-12-31')]
df2015 = df[(df['funded_at'] >= '2015-01-01') & (df['funded_at'] <= '2015-12-31')]


############################################################################
# Create a dictionary to save all startup company information in dictionary 
# Comment out because the dictionary data has been saved into Data.py
############################################################################

# startup_dict = {}

# for index, row in df2014.iterrows():
        
#     comp_industry = ""
#     comp_region = ""
#     investor = ""
#     fund_type = ""
#     fund_need = ""

#     # startup name
#     company = row['company_name'].decode('ascii','ignore').encode('ascii')

#     # startup industry
#     comp_category = row['company_category_list']
#     if str(comp_category) == 'na' and type(comp_category) == float:
#         comp_category = ["unspecified"]
#     elif str(comp_category) == 'nan' and type(comp_category) == float:
#         comp_category = ["unspecified"]
#     else: 
#         comp_category = comp_category.split("|")
#         #print type(comp_category)
#         #print comp_category

#     # startup region 
#     comp_region = row['company_region']
#     if str(comp_region) == 'na' and type(comp_region) == float:
#         comp_region = "unspecified"
#     elif str(comp_region) == 'nan' and type(comp_region) == float:
#         comp_region = "unspecified"    
        
#     comp_state_code = row['company_state_code']
#     if str(comp_state_code) == 'na' and type(comp_state_code) == float:
#         comp_state_code = "unspecified"
#     elif str(comp_state_code) == 'nan' and type(comp_state_code) == float:
#         comp_state_code = "unspecified"  
        
#     # investor name
#     investor = row['investor_name'].decode('ascii','ignore').encode('ascii')

#     # investor category
# #         investor_category = row['investor_category_list']
# #         if investor_category == ['NA'] or investor_category == ['NaN']:
# #              investor_category = "global"  

#     # investor region
# #         investor_region = row['investor_region']
# #         if investor_region == ['NA'] or investor_region == ['NaN']:
# #              investor_region = "global"  

#     # startup funding round
#     fund_type = row['funding_round_type']
#     if str(fund_type) == 'na' and type(fund_type) == float:
#         fund_type = "unspecified"
#     elif str(fund_type) == 'nan' and type(fund_type) == float:
#         fund_type = "unspecified"

#     # investor funded year
# #         year = row['funded_at'].year
# #         if year == ['NA'] or year == ['NaN']:
# #             year = "global"

#     # startup raised amount
#     fund_need = row['raised_amount_usd']
#     if str(fund_need) == 'na' and type(fund_need) == float:
#         fund_need = 0 
#     elif str(fund_need) == 'nan' and type(fund_need) == float:
#         fund_need = 0

#     if company not in startup_dict: 
#         startup_dict[company] = {"comp_category": [], "comp_region": [], "investor": [], "comp_state_code": [], "fund_type":[]}
#         startup_dict[company]['comp_region'] = [comp_region]
#         startup_dict[company]['investor'] = [investor]
#         startup_dict[company]['comp_state_code'] = [comp_state_code]
#         startup_dict[company]['fund_type'] = [fund_type]
#         startup_dict[company]['fund_need'] = fund_need
    
#         if comp_category == ["unspecified"]: 
#             startup_dict[company]['comp_category'] = comp_category
#         else: 
#             for each_category in comp_category: 
#                 if each_category in startup_dict[company]['comp_category']:
#                     pass
#                 else: 
#                     startup_dict[company]["comp_category"].append(each_category)
#                     #print ("category append: ", startup_dict[company]["comp_category"])

#     else:
#         if investor in startup_dict[company]['investor']:
#             pass 
#         else: 
#             startup_dict[company]["investor"].append(investor)

#         if comp_category == ["unspecified"]: 
#             pass
#         else: 
#             for each_category in comp_category: 
#                 if each_category in startup_dict[company]['comp_category']:
#                     pass
#                 else: 
#                     startup_dict[company]["comp_category"].append(each_category)
#                     #print ("category append: ", startup_dict[company]["comp_category"])

#         if comp_region in startup_dict[company]["comp_region"]:
#             pass 
#         else: 
#             startup_dict[company]["comp_region"].append(comp_region)

#         if fund_type in startup_dict[company]["fund_type"]:
#             pass 
#         else: 
#             startup_dict[company]["fund_type"].append(fund_type)

#         startup_dict[company]["fund_need"] += fund_need

#         if comp_state_code in startup_dict[company]["comp_state_code"]:
#             pass 
#         else: 
#             startup_dict[company]["comp_state_code"].append(comp_state_code)
            
# for key in startup_dict: 
    
#     raised_amt_usd = startup_dict[key]['fund_need']
    
#     if raised_amt_usd <= 1000:
#         pass
#     elif raised_amt_usd > 1000 and raised_amt_usd <= 50000:
#         startup_dict[key]['fund_need'] = "1000-50K"
#     elif raised_amt_usd > 50000  and raised_amt_usd <= 100000:
#         startup_dict[key]['fund_need'] = "50K-100K"
#     elif raised_amt_usd > 100000 and raised_amt_usd <= 1000000:
#         startup_dict[key]['fund_need'] = "100K-1M"
#     elif raised_amt_usd > 1000000 and raised_amt_usd <= 10000000:
#         startup_dict[key]['fund_need'] = "1M-10M"
#     elif raised_amt_usd > 10000000 and raised_amt_usd <= 100000000:
#         startup_dict[key]['fund_need'] = "10M-100M"
#     elif raised_amt_usd > 100000000:
#         startup_dict[key]['fund_need'] = "above 100M"

############################################################################
# Create a bipartite graph for startups and investors
############################################################################


import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite

df2014_copy = df2014.copy()

company_investor = []
for index, row in df2014_copy.iterrows():
    company_name = row['company_name'].decode('ascii','ignore').encode('ascii')
    investor_name = row['investor_name'].decode('ascii','ignore').encode('ascii')
    pair = (company_name, investor_name)
    company_investor.append(pair)

b = zip(*company_investor)
startups = set(b[0])
investors = set(b[1])

# Build bipartile graph
B = nx.Graph()
B.add_nodes_from(startups, bipartite=0)
B.add_nodes_from(investors, bipartite=1)
B.add_edges_from(company_investor)

top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
bottom_nodes = set(B) - top_nodes

startup = bipartite.projected_graph(B, top_nodes)
#print nx.is_connected(startup)
investor = bipartite.projected_graph(B, bottom_nodes)
#print nx.is_connected(investor)

G = nx.Graph()
for pair in company_investor:
    G.add_edge(*pair, weight=1)

# Get the shortest path between all nodes
path = nx.all_pairs_shortest_path(G)


############################################################################
# Create a dictionary to store investor information
############################################################################

investor_dict = {}
# remove funding amount below 1000
# every category count 1 
for index, row in df2014.iterrows():
        
    category = ""
    region = ""
    state = ""
    fund_type = ""
    fund_need = ""
    
    investor = row['investor_name'].decode('ascii','ignore').encode('ascii')
    company = row['company_name'].decode('ascii','ignore').encode('ascii')
    if company == 'D\xcc_nde':
        company = 'D\xc3\xb3nde'

    if investor not in investor_dict:
        investor_dict[investor] = []
        investor_dict[investor] = [company]
        
    else:
        if company in investor_dict[investor]:
            pass 
        else: 
            investor_dict[investor].append(company)

############################################################################
# Create a list of companies that appear in both 2014 and 2015. 
# Use this list of companies to test accuracy. 
############################################################################

intersection = df2014[['company_name']].merge(df2015[['company_name']]).drop_duplicates()
testing_set = list(intersection['company_name'].unique())
testing_company = []
for i in testing_set:
    i = i.decode('ascii','ignore').encode('ascii')
    testing_company.append(i)

############################################################################
# Basedline Models used as benchmark: 
# Before I develop the ranking algorithms. I first built two simple models. 
# The first model I use only similarity without using building the bipartite graph
# The second model I use only bipartite graph without considering the attributes of the company. 
############################################################################  

# The first baseline model 

count = 0
startup_copy2015 = startup_dict2015

for test_comp in startup_copy2015:
    
    record_score = {}
    
    for each_comp in startup_copy2014:

        if each_comp in testing_company: 
            score = 0
            avg_accuracy = 0

            # category
            category = startup_copy2014[each_comp]['comp_category']
            category_count = len(startup_copy2014[each_comp]['comp_category'])

            test_category = startup_copy2015[test_comp]['comp_category']
            category_overlap = len(set(category).intersection(test_category))
            category_ratio = float(category_overlap)/float(category_count)

            # state
            state = startup_copy2014[each_comp]['comp_state_code']
            state_count = len(startup_copy2014[each_comp]['comp_state_code'])    

            test_state = startup_copy2015[test_comp]['comp_state_code']
            state_overlap = len(set(state).intersection(test_state))
            state_ratio = float(state_overlap)/float(state_count)

            #region
            region = startup_copy2014[each_comp]['comp_region']
            region_count = len(startup_copy2014[each_comp]['comp_region'])    

            test_region = startup_copy2015[test_comp]['comp_region']
            region_overlap = len(set(region).intersection(test_region))
            region_ratio = float(region_overlap)/float(region_count)

            #fund_type
            fund_type = startup_copy2014[each_comp]['fund_type']
            fund_type_count = len(startup_copy2014[each_comp]['fund_type'])    

            test_fund_type = startup_copy2015[test_comp]['fund_type']
            fund_overlap = len(set(fund_type).intersection(test_fund_type))
            fund_ratio = float(fund_overlap)/float(fund_type_count) 

            #fund_amount
            fund_need = startup_copy2014[each_comp]['fund_need']
            test_fund_need = startup_copy2015[test_comp]['fund_need']

            if fund_need == test_fund_need: 
                fund_match = 1 
            else: 
                fund_match = 0

            score = category_ratio + state_ratio + region_ratio + fund_ratio + fund_match

            record_score[each_comp] = score
            
        #print record_score
        
    import operator
    top10score = dict(sorted(record_score.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
        
    #print top10score

    startup_list=[]
    for key in top10score:
        startup_list.append(key)
    #print startup_list

#         import operator
#         top10score = dict(sorted(record_score.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])

    investor_list = []
    for each in startup_list:
        potential_investor = startup_copy2014[each]['investor']
        #print potential_investor
        investor_list.extend(potential_investor)
    #print type(investor_list)
    #print investor_list
    
    investor = startup_copy2015[test_comp]['investor']
    #print type(investor)
    #print(investor)
    #print investor
    
    set_list = list(set(investor_list)&set(investor))
    accuracy = float(len(set_list))/float(10)
    
    accuracy = float(len(set(startup_copy2015[test_comp]['investor']).intersection(investor_list)))/float(10)

    if accuracy > 0:
        count += 1
        #print count

#         #only using the percentage
#         #avg_accuracy += accuracy
#             #print accuracy
    
final_accuracy = float(count)/float(len(startup_copy2015))
print "final: ", final_accuracy



############################################################################
# The second baseline model 

import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite

df2014_copy = df2014.copy()

company_investor = []
for index, row in df2014_copy.iterrows():
    company_name = row['company_name']
    investor_name = row['investor_name']
    pair = (company_name, investor_name)
    company_investor.append(pair)

b = zip(*company_investor)
startups = set(b[0])
investors = set(b[1])

# Build bipartile graph
B = nx.Graph()
B.add_nodes_from(startups, bipartite=0)
B.add_nodes_from(investors, bipartite=1)
B.add_edges_from(company_investor)

top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
bottom_nodes = set(B) - top_nodes

startup = bipartite.projected_graph(B, top_nodes)
#print nx.is_connected(startup)
investor = bipartite.projected_graph(B, bottom_nodes)
#print nx.is_connected(investor)

G = nx.Graph()
for pair in company_investor:
    G.add_edge(*pair, weight=1)

# Get the shortest path between all nodes
edge_list = G.edges()
path = nx.all_pairs_shortest_path(G)

for test_comp in testing_company: 
    # Find the Testing company's neighbor 
    test_comp_neighbors = startup.edges(test_comp)
    # Get the list of all the neighbors in the bipartile graph
    connected_startup_neighbor = [x[1] for x in test_comp_neighbors]

    investor_list = []
    for neighbor in connected_startup_neighbor: 
        for edge in edge_list: # or use the startup_dict to find past investors
            if edge[0] == neighbor: 
                investor_list.append(edge[1])
    #print set(investor_list)

    accuracy = float(len(set(startup_dict2015['SilverPush']['investor']).intersection(investor_list)))/float(10)

    if accuracy > 0:
        count += 1
        #print count

#         #only using the percentage
#         #avg_accuracy += accuracy
#             #print accuracy
    
final_accuracy = float(count)/float(len(startup_copy2015))
print "final: ", final_accuracy

############################################################################
# Ranking Algorithm 1: 
# 1. For each startup company, find the top 10 similar companies based on attributes in the dataset. 
# 2. Find the investors of its similar companies using bipartite information. 
# 3. Rank the investors based on 1) Whether it invested in the startup company before and
#    2) the number of similar companies (found in step 1) it invested in the past. 
############################################################################

total_precision_accuracy = 0
total_recall_accuracy = 0
count = 0

startup_dict2014 = startup_dict

for test_comp in testing_company:
    
    record_score = {}
    
    test_comp_neighbors = startup.edges(test_comp)
    # Get the list of all the neighbors in the bipartile graph
    connected_neighbor = [x[1] for x in test_comp_neighbors]
    
    for each_comp in startup_dict2014:

        precision_accuracy = 0
        recall_accuracy = 0

        # category
        category = startup_dict2014[each_comp]['comp_category']
        category_count = len(startup_dict2014[each_comp]['comp_category'])

        test_category = startup_dict2015[test_comp]['comp_category']
        category_overlap = len(set(category).intersection(test_category))
        category_ratio = float(category_overlap)/float(category_count)

        # state
        state = startup_dict2014[each_comp]['comp_state_code']
        state_count = len(startup_dict2014[each_comp]['comp_state_code'])    

        test_state = startup_dict2015[test_comp]['comp_state_code']
        state_overlap = len(set(state).intersection(test_state))
        state_ratio = float(state_overlap)/float(state_count)

        #region
        region = startup_dict2014[each_comp]['comp_region']
        region_count = len(startup_dict2014[each_comp]['comp_region'])    

        test_region = startup_dict2015[test_comp]['comp_region']
        region_overlap = len(set(region).intersection(test_region))
        region_ratio = float(region_overlap)/float(region_count)

        #fund_type
        fund_type = startup_dict2014[each_comp]['fund_type']
        fund_type_count = len(startup_dict2014[each_comp]['fund_type'])    

        test_fund_type = startup_dict2015[test_comp]['fund_type']
        fund_overlap = len(set(fund_type).intersection(test_fund_type))
        fund_ratio = float(fund_overlap)/float(fund_type_count) 

        #fund_amount
        fund_need = startup_dict2014[each_comp]['fund_need']
        test_fund_need = startup_dict2015[test_comp]['fund_need']

        if fund_need == test_fund_need: 
            fund_match = 1 
        else: 
            fund_match = 0

        if each_comp in connected_neighbor: 
            overlap_investor = list((set(startup_dict2014[each_comp]['investor'])&(set(startup_dict2014[test_comp]['investor']))))
            union_investor = list((set(startup_dict2014[each_comp]['investor'])|(set(startup_dict2014[test_comp]['investor']))))               
            score = category_ratio + state_ratio + region_ratio + fund_ratio + fund_match + float(len(overlap_investor))/float(len(union_investor))
        else:
            score = category_ratio + state_ratio + region_ratio + fund_ratio + fund_match               
        record_score[each_comp] = score

    import operator
    top10score = dict(sorted(record_score.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    #print top10score

    investors_list=[]
    for key in top10score:
        investors = startup_dict2014[key]["investor"]
        investors_list.extend(investors)

    top10_investor = {}
    for each_investor in investors_list:
        past_investor_score = 0
        investor_score = 0 
        #print "investor: ", each_investor
        if each_investor in startup_dict[test_comp]['investor']:
            past_investor_score = float(1)/float(len(startup_dict[test_comp]['investor']))
        #print "past_investor_score", past_investor_score
        investor_score += past_investor_score
        #print "investor_score", investor_score
        for key in top10score:
            if key in investor_dict[each_investor]: 
                investor_score += top10score[key]
                #print ("past investee", key, top10score[key])
        top10_investor[each_investor] = investor_score
        #print ("investor score: ", investor_score)
    top10_investor_score = dict(sorted(top10_investor.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    top10_investor_list = [key for key in top10_investor_score]
    print (test_comp, top10_investor_score)

    #print (startup_dict[test_comp]["investor"])

    set_list = list(set(startup_dict2015[test_comp]['investor'])&set(top10_investor_list)) # use 2015 data. 
    precision_accuracy = float(len(set_list))/float(10)   
    recall_accuracy = float(len(set_list))/float(len(startup_dict2015[test_comp]['investor']))
    #print (precision_accuracy)
    
    if precision_accuracy > 0 : 
        count += 1 
    
    total_precision_accuracy += precision_accuracy
    total_recall_accuracy += recall_accuracy   
        
print "average precision: ", float(total_precision_accuracy)/float(len(testing_company)) # divide over testing company
print "average recall: ", float(total_recall_accuracy)/float(len(testing_company))
print "average count: ", float(count)/float(len(testing_company))


############################################################################
# Ranking Algorithm 2: 
# 1. Use bipartite graph to get connected nodes (similar companies) to a startup
# 2. Look for investors of the connected nodes
# 3. Look at past history of the investors. Get a list of past investees of each investor
# 4. For each past investee, calculate the similarity score of the startup company
# 5. Sum all the similarity scores of all past investees. If the investor happens to be a past investor. Add more score. 
############################################################################

for test_comp in testing_company: 
    # Find the Testing company's neighbor 
    
    #print "test_comp", test_comp
        
    record_score = {}
    precision_accuracy = 0
    recall_accuracy = 0
    total_precision_accuracy = 0
    total_recall_accuracy = 0
    count = 0
    

    test_comp_neighbors = startup.edges(test_comp)
    # Get the list of all the neighbors in the bipartile graph
    connected_neighbor = [x[1] for x in test_comp_neighbors]
    #print("neighbor: ", connected_neighbor)

    #print "part 2"
    investors_list = []
    for neighbor in connected_neighbor: 
        if neighbor in startup_dict: 
            #print "neighbor: ", neighbor
            investors = startup_dict[neighbor]["investor"]
            #print investors
            for investor in investors:
                investors_list.append(investor)
    #print investors_list

    # ranking using similarity of investees. Second, we can also use count. 
    for each_investor in investors_list:

        investees = investor_dict[each_investor]
        #print "investor ", each_investor
        #print "investees: ", investees

        total_score = 0 #unweighted score
        past_investor_score = 0 
        cf_score = 0 

        for each_comp in investees:

            category = startup_dict[each_comp]['comp_category']
            category_count = len(startup_dict[each_comp]['comp_category'])

            test_category = startup_dict[test_comp]['comp_category']
            category_overlap = len(set(category).intersection(test_category))
            category_ratio = float(category_overlap)/float(category_count)

            # state
            state = startup_dict[each_comp]['comp_state_code']
            state_count = len(startup_dict[each_comp]['comp_state_code'])    

            test_state = startup_dict[test_comp]['comp_state_code']
            state_overlap = len(set(state).intersection(test_state))
            state_ratio = float(state_overlap)/float(state_count)

            #region
            region = startup_dict[each_comp]['comp_region']
            region_count = len(startup_dict[each_comp]['comp_region'])    

            test_region = startup_dict[test_comp]['comp_region']
            region_overlap = len(set(region).intersection(test_region))
            region_ratio = float(region_overlap)/float(region_count)

            #fund_type
            fund_type = startup_dict[each_comp]['fund_type']
            fund_type_count = len(startup_dict[each_comp]['fund_type'])    

            test_fund_type = startup_dict[test_comp]['fund_type']
            fund_overlap = len(set(fund_type).intersection(test_fund_type))
            fund_ratio = float(fund_overlap)/float(fund_type_count) 

            #fund_amount
            fund_need = startup_dict[each_comp]['fund_need']
            test_fund_need = startup_dict[test_comp]['fund_need']

            if fund_need == test_fund_need: 
                fund_match = 1 
            else: 
                fund_match = 0

            score = category_ratio + state_ratio + region_ratio + fund_ratio + fund_match

            total_score += score

        cf_score = float(total_score)/float(len(investees))

        if each_investor in startup_dict[test_comp]['investor']:
            past_investor_score = float(1)/float(len(startup_dict[test_comp]['investor'])) # why ratio, not just add one?
            cf_score += past_investor_score

        #print (each_investor, ", score: ", cf_score)

        record_score[each_investor] = cf_score

    #print record_score

    import operator
    top10score = dict(sorted(record_score.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])

    top10_list=[]
    for key in top10score:
        top10_list.append(key)

    #print "top10: ", top10_list

    set_list = list(set(startup_dict2015[test_comp]['investor'])&set(top10_list)) # use 2015 data. 
    precision_accuracy = float(len(set_list))/float(10)
    recall_accuracy = float(len(set_list))/float(len(startup_dict2015[test_comp]['investor']))
    count += 1
    
    if accuracy > 0:
        count += 1 

    print (test_comp, ": ", accuracy)
    total_precision_accuracy += precision_accuracy
    total_recall_accuracy += recall_accuracy
    
print "average precision: ", float(total_precision_accuracy)/float(len(testing_company)) # divide over testing company
print "average recall: ", float(total_recall_accuracy)/float(len(testing_company))
print "average count: ", float(count)/float(len(testing_company))
  


