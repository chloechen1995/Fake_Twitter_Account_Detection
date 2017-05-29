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
#%%
import t_analysis as ta
import similarity_1 as sim_1
import similarity_2 as sim_2


#%%
sample_data_id = pd.read_csv(open("/Users/Chloechen/Desktop/tweet_analysis/sample_data.csv", 'rU'), encoding = 'utf-8', usecols = ['id'])

sample_id = sample_data_id['id'].tolist()

#%%
os.chdir('/Users/Chloechen/Desktop/Sample_Tweets')

sample_id_exist = []
for s_id in sample_id:
    if os.path.exists(str(s_id) + "_tweets_.csv"):
        sample_id_exist.append(s_id)

#%%
sample_tweet_analysis = pd.DataFrame(sample_id_exist, columns = ["twitter_id"])
#%%
sample_tweet_analysis['similarity_ratio_1'] = sample_tweet_analysis["twitter_id"].apply(sim_1.tweet_sim)

#%%
sample_tweet_analysis['url_rtio'] = sample_tweet_analysis["twitter_id"].apply(ta.url_ratio)
sample_tweet_analysis['url_unique_ratio'] = sample_tweet_analysis["twitter_id"].apply(ta.url_unique_ratio)
sample_tweet_analysis['hashtag_ratio'] = sample_tweet_analysis["twitter_id"].apply(ta.hashtag_ratio)
sample_tweet_analysis['username_ratio'] = sample_tweet_analysis["twitter_id"].apply(ta.username_ratio)
sample_tweet_analysis['username_unique_ratio'] = sample_tweet_analysis["twitter_id"].apply(ta.username_unique_ratio)
sample_tweet_analysis['similarity_ratio_1'] = sample_tweet_analysis["twitter_id"].apply(sim_1.tweet_sim)
sample_tweet_analysis['similarity_ratio_2'] = sample_tweet_analysis["twitter_id"].apply(sim_2.sim_formula)

#%%
os.chdir('/Users/Chloechen/Desktop/tweet_analysis')
sample_tweet_analysis.to_csv("sample_tweet_analysis.csv", sep=',')