#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 21:03:53 2017

@author: Rachel
"""
#%%

########## Subset Sample Data
# The sample data is consisted of 2900 genuine accounts and 350 fake/spam accounts.
# In this case, we try to be close to the proportion of fake/spam accounts in real situation.

import os
import glob
import re
os.chdir('/Users/Rachel/Desktop/STA 160/sample_data_2')
all_files = []
files = glob.glob('*followers.csv')
for file_name in files:
    user_id = re.search(r'[0-9]+', file_name).group(0)
    all_files.append(user_id)
    
all_ids = [int(user_id) for user_id in all_files]
#%%
import pandas as pd
os.chdir('/Users/Rachel/Desktop/STA 160')
full_data = pd.read_csv('final data.csv', index_col = 0)
par_data = full_data[full_data.id.isin(all_ids)]

#%%
import cPickle
f = open('eig_ctr.pl','r')
eig_ctr = cPickle.load(f)
f.close()
#%%
eig_crt_dict = {}
for k in all_files:
    try:
        eig_crt_dict[k] = eig_ctr[k]
    except KeyError:
        pass
#%%
eig_crt_dict2 = {}
for k in all_files_m:
    try:
        eig_crt_dict2[k] = eig_ctr[k]
    except KeyError:
        pass
#%%
id_list = [int(user_id) for user_id in eig_crt_dict.keys()]

#%%
par_data_fake = par_data[par_data.label == 'fake_users'] #2629
par_data_genu = par_data[par_data.label == 'genuine'] #2900
par_data_sspam1 = par_data[par_data.label == 'new social_spambots_1'] #89
par_data_sspam2 = par_data[par_data.label == 'new social_spambots_2'] #3187
par_data_sspam3 = par_data[par_data.label == 'new social_spambots_3'] #458
par_data_tspam1 = par_data[par_data.label == 'new traditional_spambots_1'] #778
par_data_tspam3 = par_data[par_data.label == 'new traditional_spambots_3'] #389
par_data_tspam4 = par_data[par_data.label == 'new traditional_spambots_4'] #1126 
#%%
sample_fake = par_data_fake.sample(n = 50, random_state = 5)
sample_genu = par_data_genu.sample(n = 2900, random_state = 5)
sample_sspam1 = par_data_sspam1.sample(n= 50, random_state = 5)
sample_sspam2 = par_data_sspam2.sample(n = 50, random_state = 5)
sample_sspam3 = par_data_sspam3.sample(n = 50, random_state = 5)
sample_tspam1 = par_data_tspam1.sample(n = 50, random_state = 5)
sample_tspam3 = par_data_tspam3.sample(n = 50, random_state = 5)
sample_tspam4 = par_data_tspam4.sample(n = 50, random_state = 5)
sample = pd.concat([sample_fake, sample_genu, sample_sspam1,sample_sspam2, sample_sspam3, sample_tspam1, sample_tspam3, sample_tspam4])
#%%
sample.to_csv('sample_data.csv')
#%%
full_data_genu = full_data[full_data.label == 'genuine'] 
genu_diff = set(full_data_genu.id).difference(par_data_genuine.id)
#%%
import cPickle
f = open('genu_diff.pl','w')
cPickle.dump(genu_diff, f)
f.close()
#%%
#%%
sd2 = pd.read_csv('sample_data.csv')
for user_id in sd2.id:
    try:
        file_name = './sample_data_2/' + str(user_id) + '_followings.csv'
        df = pd.read_csv(file_name, index_col = 0)
        df.to_csv('./graph_tool/sample_data/' + str(user_id) + '_followings.csv')
    except IOError:
        print file_name
        pass
