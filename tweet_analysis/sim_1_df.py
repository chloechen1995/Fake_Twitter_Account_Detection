#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 07:47:42 2017

@author: Chloechen
"""

### This scirpt creates a dataframe for storing the tweet similarity ratio 1 result

#%%
import pandas as pd
import similarity_1 as sim_1
from pandas.io.common import CParserError
import numpy as np
#%%
sample_data_id = pd.read_csv(open("sample_data_1.csv", 'rU'), encoding = 'utf-8', usecols = ['id'])
sample_data_id['id'] = sample_data_id['id'].astype(int)
sample_id = sample_data_id['id'].tolist()

#%%
path = r'Sample_Tweets/'

sample_names = [i + '_tweets.csv' for i in list(sample_data_id['id'].astype(str))]

sample_tw = []

for i in sample_names:
    try:
        address = path + i
        df = pd.read_csv(address)
        sample_tw.append(df)
    except (CParserError, IOError): 
        sample_tw.append([])

#%%
similarity_ratio_1 = [sim_1.tweet_sim(sample_tw[int(i)]) for i in range(len(sample_tw))]

similarity_ratio_1_df = pd.DataFrame(np.column_stack([sample_id, similarity_ratio_1]), 
                                     columns = ["id", "similarity_ratio_1"])
#%%
similarity_ratio_1_df.to_csv("similarity_ratio_1.csv", sep=',')