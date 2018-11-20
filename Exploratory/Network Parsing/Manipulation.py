# !/usr/bin/env python
# -*- coding: utf-8 -*

import networkx as nx
import matplotlib.pyplot as plt
import pydot
import sqlite3
import sys
from datetime import datetime
from wordcloud import WordCloud


reload(sys)
sys.setdefaultencoding('utf8')

'''Setup Database'''
url_num = 0
fname_networks_schools = 'startups_founder_networks_total_schools.csv'
fname_networks_companies = 'startups_founder_networks_total_companies.csv'
fname_skills_skills = 'startups_founder_skills_total_skills.csv'
fname_skills_position = 'startups_founder_skills_total_position.csv'
fname_influence = 'startups_founder_influence_total.csv'
fname_funding = 'startups_funding_total.csv'

# founder_networks = {}
# founder_skills = {}
# founder_influence = {}
# funding = {}
# columns = ['Company_Name', 'Founder', 'School', 'Former_Companies', 'Major', 'Former_Position', 'Top_Skills', 'Tweets', 'Following', 'Followers', 'Retweets', 'Likes', 'Linkedin', 'Twitter']
# dataset = [(fname_networks, founder_networks), (fname_skills, founder_skills), (fname_influence, founder_influence), (fname_funding, funding)]

conn = sqlite3.connect('startups.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS founder_networks_schools')
c.execute('DROP TABLE IF EXISTS founder_networks_companies')
c.execute('DROP TABLE IF EXISTS founder_skills_skills')
c.execute('DROP TABLE IF EXISTS founder_skills_position')
c.execute('DROP TABLE IF EXISTS founder_influence')
c.execute('DROP TABLE IF EXISTS funding')
c.execute('CREATE TABLE founder_networks_schools(Company_Name TEXT, Founder TEXT, Schools TEXT)')
c.execute('CREATE TABLE founder_networks_companies(Company_Name TEXT, Founder TEXT, Former_Companies TEXT)')
c.execute('CREATE TABLE founder_skills_skills(Company_Name TEXT, Founder TEXT, Skills TEXT)')
c.execute('CREATE TABLE founder_skills_position(Company_Name TEXT, Founder TEXT, Former_Position TEXT)')
c.execute('CREATE TABLE founder_influence(Company_Name TEXT, Founder TEXT, Tweets INT, Following INT, Followers INT, Retweets TEXT, Likes TEXT, Twitter TEXT)')
c.execute('CREATE TABLE funding(Company_Name TEXT, Round INT, Type TEXT, Funding_Date TEXT, Amount TEXT, News TEXT, Investors TEXT, Investor_Location TEXT)')

with open(fname_networks_schools, 'rU') as f:
	for line in f:
		line = unicode(line).split(',')
		c.execute("INSERT INTO founder_networks_schools VALUES (?,?,?)", line)
with open(fname_networks_companies, 'rU') as f:
	for line in f:
		line = unicode(line).split(',')
		c.execute("INSERT INTO founder_networks_companies VALUES (?,?,?)", line)
with open(fname_skills_skills, 'rU') as f:
	for line in f:
		line = unicode(line).split(',')
		c.execute("INSERT INTO founder_skills_skills VALUES (?,?,?)", line)
with open(fname_skills_position, 'rU') as f:
	for line in f:
		line = unicode(line).split(',')
		c.execute("INSERT INTO founder_skills_position VALUES (?,?,?)", line)
with open(fname_influence, 'rU') as f:
	for line in f:
		line = unicode(line).split(',')
		c.execute("INSERT INTO founder_influence VALUES (?,?,?,?,?,?,?,?)", line)
with open(fname_funding, 'rU') as f:
	for line in f:
		line = unicode(line).split(',')
		c.execute("INSERT INTO funding VALUES (?,?,?,?,?,?,?,?)", line)			

conn.commit()

'''Networks'''

## Graph 1: schools
school_networks = c.execute('''SELECT founder_networks_schools.Company_Name, founder_networks_schools.Founder, founder_networks_schools.Schools,
                                      funding.Investors, funding.Type, funding.Round
							   FROM founder_networks_schools JOIN funding ON (founder_networks_schools.Company_Name=funding.Company_Name) 
							   WHERE founder_networks_schools.Schools IS NOT NUll
						   ''')
# AND funding.Type NOT IN ('No Stage', 'Seed')
graph1 = {}
graph1_1 = {}
temp = sorted([i for i in school_networks if i[2]], key=lambda x:(x,x[-1]))
for i in temp:
	if i[0] == 'Company Name':
		continue
	if i[-1] == 0:
		graph1[i[0]] = graph1.get(i[0],[]) + i[2].strip().split('|')
for comp in graph1:
	count = {}
	for s in graph1[comp]:
		count[s] = count.get(s,0)+1
	graph1[comp] = count.items()

TEXT1 = ','.join([j[0] for i in graph1.values() for j in i]).replace('College','').replace('University','').replace('Institute','').replace('State','').replace('School','').replace('Technology','')
wc = WordCloud().generate(TEXT1)
wc.to_file('schools.png')

G1 = nx.Graph()
for i in graph1:
	for j in graph1[i]:
		G1.add_node(j[0], att='school')
		G1.add_node(i, att='startup')
		G1.add_edge(i, j[0], weight=j[1])
def change_color(tup):
	if tup[1]['att'] == 'school':
		return 'lightblue'
	else:
		return 'lightgreen'
def change_label(tup):
	if tup[1]['att'] == 'school':
		return tup[0]
	else:
		return ''
G1.add_weighted_edges_from([(i, j[0], j[1]) for i in graph1 for j in graph1[i]])
G1_lc = max(nx.connected_component_subgraphs(G1), key=len)
dc1 = nx.degree(G1_lc)
colorarray1 = [change_color(x) for x in G1_lc.nodes(data=True)]
labelarray1 = [change_label(x) for x in G1_lc.nodes(data=True)]
nx.draw_networkx(G1_lc, with_labels=True, node_size=500, node_color=colorarray1, font_size=12)
plt.show()


# colorarray2 = [change_color(x) for x in G1.nodes(data=True)]
# nx.draw_networkx(G1, with_labels=False, node_size=40, node_color=colorarray2)


# nx.draw_networkx(G1, with_labels=False, node_size=sizearray1, node_color=colorarray1, font_size=4)
# plt.show()


# output1 = 'school_networks.dot'
# graph1_draw = pydot.Dot(graph_type='graph', charset="utf8")
# for i in graph1:
# 	for j in graph1[i]:
# 		graph1_draw.add_edge(pydot.Edge(i,j[0]))
# graph1_draw.write(output1)

# ## Graph 2: former companies
# company_networks = c.execute('''SELECT founder_networks_companies.Company_Name, founder_networks_companies.Founder, founder_networks_companies.Former_Companies,
#                                       funding.Investors, funding.Type, funding.Round
# 							   FROM founder_networks_companies JOIN funding ON (founder_networks_companies.Company_Name=funding.Company_Name) 
# 							   WHERE founder_networks_companies.Former_Companies IS NOT NUll
# 						   ''')
# graph2 = {}
# temp = sorted([i for i in company_networks if i[2]], key=lambda x:(x,x[-1]))
# for i in temp:
# 	if i[-1] == 0:
# 		graph2[i[0]] = graph2.get(i[0],[]) + i[2].strip().split('|')

# TEXT2 = ','.join([j for i in graph2.values() for j in i])
# wc = WordCloud().generate(TEXT2)
# wc.to_file('schools.png')

# for comp in graph2:
# 	count = {}
# 	for co in graph2[comp]:
# 		count[co] = count.get(co,0)+1
# 	graph2[comp] = count.items()
# # print graph2

# G2 = nx.DiGraph()
# G2.add_weighted_edges_from([(i, j[0], j[1]) for i in graph2 for j in graph2[i]])
# dc2 = nx.degree_centrality(G2)
# sizearray2 = [dc2[x] * 1000 for x in dc2]
# colorarray2 = [(dc2[x],dc2[x],dc2[x]) for x in dc2]
# nx.draw_networkx(G2, with_labels=False, node_size=sizearray2, node_color=colorarray2)

# output2 = 'company_networks.dot'
# graph2_draw = pydot.Dot(graph_type='digraph', charset="utf8")
# for i in graph2:
# 	for j in graph2[i]:
# 		graph2_draw.add_edge(pydot.Edge(i,j[0]))
# graph2_draw.write(output2)


'''Skills'''
# majors = c.execute('''SELECT Majors FROM founder_skills WHERE Majors IS NOT NUll''')
# former_position = c.execute('''SELECT DISTINCT COUNT(Former_Position) FROM founder_skills WHERE Former_Position IS NOT NUll''')
# skills = c.execute('''SELECT Skills FROM founder_skills WHERE Skills IS NOT NUll''')

# for i in majors:
# 	print i











# '''TOTAL DATASET VISULIZATION'''
# total_markets = {}
# total_location = {}
# total_signal = {}
# total_stage = {}
# total_raised = {}
# with open('startups_info_total_2.csv', 'rU') as f:
# 	for line in f:
# 		line = line.split(',')
# 		total_markets[line[5]] = total_markets.get(line[5], 0) + 1
# 		total_location[line[4]] = total_location.get(line[4], 0) + 1
# 		total_signal[line[3]] = total_signal.get(line[3], 0) + 1
# 		total_stage[line[-2]] = total_stage.get(line[-2], 0) + 1
# 		total_raised[line[-1]] = total_raised.get(line[-1], 0) + 1
# with open('startups_info_total_2_output_mkt.csv', 'wb') as f:
# 	for i in total_markets.items():
# 		f.write('{},{}\n'.format(*i))
# with open('startups_info_total_2_output_loc.csv', 'wb') as f:
# 	for i in total_location.items():
# 		f.write('{},{}\n'.format(*i))
# with open('startups_info_total_2_output_sig.csv', 'wb') as f:
# 	for i in total_signal.items():
# 		f.write('{},{}\n'.format(*i))
# with open('startups_info_total_2_output_stage.csv', 'wb') as f:
# 	for i in total_stage.items():
# 		f.write('{},{}\n'.format(*i))
# with open('startups_info_total_2_output_raised.csv', 'wb') as f:
# 	for i in total_raised.items():
# 		f.write('{},{}\n'.format(*i))
