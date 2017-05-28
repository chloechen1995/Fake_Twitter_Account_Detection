#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 21:46:44 2017

@author: Rachel
"""

########## Build Network by Package graph_tool
from graph_tool.all import *
import graph_tool.util
import pandas as pd
import re

#%%
def build_edges():
    g = Graph()
    vprop = g.new_vertex_property('string')
    for user_id in sd2.id:
        try:
            file_name_r = './sample_data/' + str(user_id) + '_followers.csv'
            file_name_i = './sample_data/' + str(user_id) + '_followings.csv'
            df_r = pd.read_csv(file_name_r, index_col = 0)
            df_i = pd.read_csv(file_name_i, index_col = 0)
            df_r.columns = ['followers']
            df_i.columns = ['followings']
            
            # assign user id to vertex
            v0 = g.add_vertex()
            vprop[v0] = str(user_id)
    
            for fol in df_r.followers:
                v = g.add_vertex()
                vprop[v] = str(fol)
                # build edge 
                g.add_edge(v, v0)

            for fol in df_i.followings:
                v = g.add_vertex()
                vprop[v] = str(fol)
                # build edge 
                g.add_edge(v0, v)

        except (ValueError, IOError):
            print user_id
            pass
    g.vp.userid = vprop
    return g

#%%
sd2 = pd.read_csv('sample_data_2.csv')
g = build_edges()

#%%
import cPickle
f = open('graph.pl','w')
cPickle.dump(g, f)
f.close()
#%%
userid_dict = {g.vp.userid[v]: v for v in g.get_vertices()}

f1 = open('userid_dict.pl', 'w')
cPickle.dump(userid_dict, f1)
f1.close()

########## Pagerank
import numpy as np
from graph_tool.all import *
import graph_tool.centrality
import pandas as pd
import cPickle
from joblib import Memory
import os
os.chdir('/Users/Rachel/Desktop/STA 160/graph_tool')
import logging as log
log.basicConfig(filename = "log_pr.txt", level = log.INFO, format='%(asctime)s %(message)s')
#%%
mem = Memory('./graph_cache')

@mem.cache

def load_file(perl_file):
    f = open(perl_file,'r')
    g = cPickle.load(f)
    f.close()
    return g
   
g = load_file('graph.pl')
userid_dict = load_file('userid_dict.pl')
#%%
sd = pd.read_csv('sample_data.csv')
userid_dict_sample = {}
for k in sd.id:
    try:
        userid_dict_sample[str(k)] = userid_dict[str(k)]
    except KeyError:
        userid_dict_sample[str(k)] = np.nan
#%%
pr = pagerank(g)
pagerank_dict = {v: pr[v] for v in g.get_vertices()}

pagerank_dict_sample = {}
for i, k in enumerate(userid_dict_sample.keys()):
    try:
        pagerank_dict_sample[str(k)] = pagerank_dict[userid_dict_sample[str(k)]]
        if ((i+1) % 100 == 0):
            info = str(i) + ' Succeed'
            log.info(info)
    except KeyError:
		pagerank_dict_sample[str(k)] = np.nan
#%%
df_pr = pd.DataFrame.from_dict(pagerank_dict_sample, orient='index')
df_pr.to_csv('df_pr.csv')

########## Eigenvector
import numpy as np
from graph_tool.all import *
import graph_tool.centrality
import pandas as pd
import cPickle
from joblib import Memory
import os
os.chdir('/Users/Rachel/Desktop/STA 160/graph_tool')
import logging as log
log.basicConfig(filename = "log_eig.txt", level = log.INFO, format='%(asctime)s %(message)s')
#%%
mem = Memory('./graph_cache')

@mem.cache

def load_file(perl_file):
    f = open(perl_file,'r')
    g = cPickle.load(f)
    f.close()
    return g
   
g = load_file('graph.pl')
userid_dict = load_file('userid_dict.pl')
#%%
#%%
sd = pd.read_csv('sample_data.csv')
userid_dict_sample = {}
for k in sd.id:
    try:
        userid_dict_sample[str(k)] = userid_dict[str(k)]
    except KeyError:
        userid_dict_sample[str(k)] = np.nan
#%%
eig_val, eig_vec = eigenvector(g)
eig_dict = {v: eig_vec[v] for v in g.get_vertices()}

eig_dict_sample = {}
for i, k in enumerate(userid_dict_sample.keys()):
    try:
        eig_dict_sample[str(k)] = eig_dict[userid_dict_sample[str(k)]]
        if ((i+1) % 100 == 0):
            info = str(i) + ' Succeed'
            log.info(info)
    except KeyError:
		eig_dict_sample[str(k)] = np.nan
#%%
df_eig = pd.DataFrame.from_dict(eig_dict_sample, orient='index')
df_eig.to_csv('df_eig.csv')
