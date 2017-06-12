#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 20:13:26 2017

@author: Chloechen
"""


### This script creates a csv file that contains the tweet analysis ratios


#%%
import pandas as pd
import t_analysis as ta
from pandas.parser import CParserError
import numpy as np

#%%
sample_data_id = pd.read_csv(open("sample_data_1.csv", 'rU'), encoding = 'utf-8', usecols = ['id'])

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
url_ratio = [ta.url_ratio(sample_tw[int(i)]) for i in range(len(sample_tw))]

#%%
url_unique_ratio = [ta.url_unique_ratio(sample_tw[int(i)]) for i in range(len(sample_tw))]

#%%
hashtag_ratio = [ta.hashtag_ratio(sample_tw[int(i)]) for i in range(len(sample_tw))]

#%%
username_ratio = [ta.username_ratio(sample_tw[int(i)]) for i in range(len(sample_tw))]

#%%
username_unique_ratio = [ta.username_unique_ratio(sample_tw[int(i)]) for i in range(len(sample_tw))]

#%%
sample_tweet_analysis_ratio = pd.DataFrame(np.column_stack([sample_id, url_ratio, url_unique_ratio, hashtag_ratio, username_ratio, username_unique_ratio]), 
                                     columns = ["id", "url_ratio", "url_unique_ratio", "hashtag_ratio", "username_ratio", "username_unique_ratio"])

#%%
sample_tweet_analysis_ratio.to_csv("t_analysis_ratio_2.csv", sep=',')




