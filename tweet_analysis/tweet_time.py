#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:34:21 2017

@author: Chloechen
"""

#%%
import pandas as pd
from pandas.parser import CParserError
import os 
import numpy as np
#%%
os.chdir("/Users/Chloechen/Desktop/tweet_analysis/data")
sample_data_id = pd.read_csv(open("sample_data.csv", 'rU'), encoding = 'utf-8', usecols = ['id'])
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
final_df = pd.concat([pd.DataFrame(i) for i in sample_tw])
#%%
final_df.Created_At = final_df.Created_At.apply(pd.to_datetime)

final_df['delta'] = (final_df['Created_At'].shift(1) - final_df['Created_At']).astype('timedelta64[s]')

#%%
final_df.loc[final_df.index == 0, 'delta'] = np.nan
#%%
tweet_time = final_df.groupby('User_Id', as_index=False).agg({'delta': [np.sum, np.mean, np.max, np.min]})
tweet_time = tweet_time.reset_index()
tweet_time.columns = tweet_time.columns.droplevel()
tweet_time.columns = ['index_1', 'id', 'tweet_time_sum', 'tweet_time_mean', 'tweet_time_max', 'tweet_time_min']
#%%
tweet_time.to_csv("tweet_time_dff.csv", sep = ",")