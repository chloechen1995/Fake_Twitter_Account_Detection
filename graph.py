#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 21:46:44 2017

@author: Rachel
"""

# Build Network by Package graph_tool

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