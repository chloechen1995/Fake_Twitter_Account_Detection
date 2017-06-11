#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:34:21 2017

@author: Chloechen
"""

### This script calculates the time difference between two consecutive tweets
#%%
import pandas as pd
from pandas.parser import CParserError
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
sample_unique = sample_data_id.id.unique()
tweet_time_unique = tweet_time.id.unique()
diff = np.setdiff1d(sample_unique, tweet_time_unique)
diff_list = diff.tolist()
#%%
diff_df = pd.DataFrame(diff_list, columns = ['id'])
#%%
diff_df = diff_df.reindex(columns=list(tweet_time.columns), fill_value="No tweets")
#%%

final_time_df = pd.concat([diff_df, tweet_time], ignore_index=True)
final_time_df['id'] = final_time_df['id'].astype(np.int64)
#%%
final_time_df.to_csv("tweet_time_dff_1.csv", sep = ",")