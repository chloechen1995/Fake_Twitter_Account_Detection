#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 20:13:26 2017

@author: Chloechen
"""
#%%
import os
import pandas as pd
os.chdir('/Users/Chloechen/Desktop')
import glob
import tweet_analysis as ta
import similarity_1 as sim_1
# import similarity_2 as sim_2
#%%

#%%
sample_data_id = pd.read_csv(open("/Users/Chloechen/Desktop/sample_data.csv", 'rU'), encoding = 'utf-8', usecols = ['id'])

sample_id = sample_data_id['id'].tolist()

sample_id.sort()
    
#%%

tweetfile = ["%s_tweets.csv" %str(user_id) for user_id in sample_id]
#%%

# Only select the most recent 200 tweets
sample = "/Users/Chloechen/Desktop/Sample"
for csvfile in sample:
    base = '/Users/Chloechen/Desktop/Sample_Tweets'
    files = glob.glob('*.csv')
    
    for file_name in files:
        os.chdir(path)
        try:
            df_200 = pd.read_csv(file_name, nrows = 200)
        except pd.parser.CParserError:
            df_200 = pd.read_csv(file_name)
        os.chdir(base)
        df_200.to_csv(file_name)  
#%%
sample_id_test = sample_id[1:3]
#%%
os.chdir(sample)
#%%
for sample_id in sample_id_test:
    print ta.url_ratio(sample_id)
    
#%%
for sample_id in sample_id_test:
    print sim_1.tweet_sim(sample_id)
    
    
    
    