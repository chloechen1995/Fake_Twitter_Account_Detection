#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 07:53:04 2017

@author: Chloechen
"""

# Reference: https://chrisalbon.com/machine-learning/random_forest_classifier_example_scikit.html
#%%
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
#%%
os.chdir("/Users/Chloechen/Desktop/tweet_analysis")
user_features = pd.read_csv("sample_feature_guanyu.csv")
user_features['id'] = user_features['id'].astype(int)
user_features = user_features.drop('Unnamed: 0', 1)
network_features = pd.read_csv("sample_data_rachel.csv")
network_features = network_features.rename(columns = {'Unnamed: 0': 'id'})
network_features['id'] = network_features['id'].astype(int)
t_analysis_ratio = pd.read_csv("t_analysis_ratio.csv")
t_analysis_ratio = t_analysis_ratio.drop('Unnamed: 0', 1)
t_analysis_ratio['id'] = t_analysis_ratio['id'].astype(int)
similarity_ratio_1 = pd.read_csv("similarity_ratio_1.csv")
similarity_ratio_1 = similarity_ratio_1.drop('Unnamed: 0', 1)
similarity_ratio_1['id'] = similarity_ratio_1['id'].astype(int)
similarity_ratio_2 = pd.read_csv("similarity_ratio_2.csv")
similarity_ratio_2 = similarity_ratio_2.drop('Unnamed: 0', 1)
similarity_ratio_2['id'] = similarity_ratio_2['id'].astype(int)

user_tweets = t_analysis_ratio.merge(similarity_ratio_1, on = 'id').merge(similarity_ratio_2, on = 'id')
#%%
final_df = user_features.merge(network_features, on = 'id').merge(user_tweets, on = 'id')

#%%
final_df['no_tweet'] = np.where(final_df['similarity_ratio_1'] == "None", 1, 0)
#%%
final_df = final_df.replace([np.inf, -np.inf], np.nan)
final_df = final_df.replace({'No tweets': -1}, regex = True)
final_df = final_df.replace({'None': -1}, regex = True)
final_df = final_df.fillna(-1)

#%%
final_df[['tweet_rate', 'mobile_ratio', 'website_ratio', 'third_ratio', 'other_ratio', 'url_ratio', 'url_unique_ratio', 'hashtag_ratio', 'username_ratio', 'username_unique_ratio', 'similarity_ratio_1', 'similarity_ratio_2']] = final_df[['tweet_rate', 'mobile_ratio', 'website_ratio', 'third_ratio', 'other_ratio', 'url_ratio', 'url_unique_ratio', 'hashtag_ratio', 'username_ratio', 'username_unique_ratio', 'similarity_ratio_1', 'similarity_ratio_2']].astype(float)
#%%
cols = list(final_df.columns.values)
cols.pop(cols.index('label'))
final_df = final_df[cols+ ['label']]
#%%
features = final_df.columns[1:-1]

#%%
# create training and test data
final_df['is_train'] = np.random.uniform(0, 1, len(final_df)) <= .80

#%%
train, test = final_df[final_df['is_train']==True], final_df[final_df['is_train']==False]     
y = pd.factorize(train['label'])[0]
#%%
# Create a random forest classifiers
clf = RandomForestClassifier(n_jobs=2)

clf.fit(train[features], y)

#%%
# Apply classifier we trained to the test data
clf.predict(test[features])

#%%
# Evaluate Classifier
preds = final_df.label[clf.predict(test[features])]

#%%
# A list of features and their importance scores
feature_list = list(zip(train[features], clf.feature_importances_))
feature_df = pd.DataFrame(feature_list, columns = ["Features", "Feature_importance"])

#%%
feature_df.sort(['Feature_importance'], ascending = False)