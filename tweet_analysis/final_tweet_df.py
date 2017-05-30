#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 20:13:26 2017

@author: Chloechen
"""

"""
Create a csv file that contains the tweet analysis results
"""

#%%
import os
import pandas as pd
os.chdir("/Users/Chloechen/Desktop/tweet_analysis")
import t_analysis as ta
import similarity_1 as sim_1
import similarity_2 as sim_2
from pandas.parser import CParserError
import numpy as np

#%%
sample_data_id = pd.read_csv(open("/Users/Chloechen/Desktop/tweet_analysis/sample_data.csv", 'rU'), encoding = 'utf-8', usecols = ['id'])

sample_id = sample_data_id['id'].tolist()

#%%
path = r'/Users/Chloechen/Desktop/Sample_Tweets/'

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
similarity_ratio_1 = [sim_1.tweet_sim(sample_tw[int(i)]) for i in range(len(sample_tw))]

#%%
similarity_ratio_2 = [sim_2.sim_formula(sample_tw[int(i)]) for i in range(len(sample_tw))]
#%%
#sample_tweet_analysis = pd.DataFrame(np.column_stack([sample_id, url_ratio, hashtag_ratio, username_ratio, username_unique_ratio]), 
#                                     columns = ["twitter_id", "url_unique_ratio", "hashtag_ratio", "username_ratio", "username_unique_ratio"])


#%%
sample_tweet_analysis = pd.DataFrame(np.column_stack([sample_id, url_ratio, hashtag_ratio, username_ratio, username_unique_ratio, similarity_ratio_1, similarity_ratio_2]), 
                                     columns = ["twitter_id", "url_unique_ratio", "hashtag_ratio", "username_ratio", "username_unique_ratio", "similarity_ratio_1", "similarity_ratio_2"])

#%%
os.chdir('/Users/Chloechen/Desktop/tweet_analysis')
sample_tweet_analysis.to_csv("sample_tweet_analysis.csv", sep=',')