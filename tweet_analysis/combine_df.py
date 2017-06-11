#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 10:19:49 2017

@author: Chloechen
"""

### This scripts combines all the feature results into a dataframe
#%%
import pandas as pd
import numpy as np

user_features = pd.read_csv("sample_feature_guanyu_1.csv")
user_features = user_features.drop('Unnamed: 0', 1)
network_features = pd.read_csv("sample_data_rachel_1.csv")
network_features = network_features.rename(columns = {'Unnamed: 0': 'id'})
#%%
t_analysis_ratio = pd.read_csv("t_analysis_ratio_1.csv").reset_index()
t_analysis_ratio = t_analysis_ratio.drop('Unnamed: 0', 1)
similarity_ratio_1 = pd.read_csv("similarity_ratio_1_1.csv")
similarity_ratio_1 = similarity_ratio_1.drop('Unnamed: 0', 1)
similarity_ratio_2 = pd.read_csv("similarity_ratio_2_1.csv")
similarity_ratio_2 = similarity_ratio_2.drop('Unnamed: 0', 1)
#%%
tweet_time = pd.read_csv("tweet_time_dff_1.csv")
tweet_time = tweet_time.drop(['index_1'], 1)

#%%
user_tweets = t_analysis_ratio.merge(similarity_ratio_1, on = 'id', how = "inner").merge(similarity_ratio_2, on = 'id', how = "inner").merge(tweet_time, on = 'id', how = "inner")
user_tweets['id'] = user_tweets['id'].astype(np.int)
#%%
final_df = user_features.merge(network_features, on = 'id').merge(user_tweets, on = 'id')

final_df['no_tweet'] = np.where(final_df['similarity_ratio_1'] == "None", 1, 0)

#%%
final_df = final_df.replace([np.inf, -np.inf], 1000000)
final_df = final_df.replace({'No tweets': -1}, regex = True)
final_df = final_df.replace({'None': -1}, regex = True)
final_df = final_df.fillna(-1)

#%%
final_df[['tweet_rate', 'mobile_ratio', 'website_ratio', 'third_ratio', 'other_ratio', 'url_ratio', 'url_unique_ratio', 'hashtag_ratio', 'username_ratio', 'username_unique_ratio', 'similarity_ratio_1', 'similarity_ratio_2', 'tweet_time_sum', 'tweet_time_mean', 'tweet_time_max', 'tweet_time_min']] = final_df[['tweet_rate', 'mobile_ratio', 'website_ratio', 'third_ratio', 'other_ratio', 'url_ratio', 'url_unique_ratio', 'hashtag_ratio', 'username_ratio', 'username_unique_ratio', 'similarity_ratio_1', 'similarity_ratio_2', 'tweet_time_sum', 'tweet_time_mean', 'tweet_time_max', 'tweet_time_min']].astype(float)
#%%
cols = list(final_df.columns.values)
cols.pop(cols.index('label'))
final_df = final_df[cols+ ['label']]
final_df['label_model'] = np.where(final_df['label'] == 'genuine', 'Genuine', 'Fake')
final_df = final_df.drop(['index','Unnamed: 0'], 1)
#%%
final_df.to_csv("final_df_sample_1.csv", sep = ",")