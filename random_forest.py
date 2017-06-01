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
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.model_selection import cross_val_predict
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
features_df = final_df[final_df.columns[1:-1]]

#%%
X = features_df.as_matrix()
# convert each label into digits

y = pd.factorize(final_df['label'])[0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

#%%
# Train the random forest classifier
clf = RandomForestClassifier(n_jobs = 2)
clf.fit(X_train, y_train)

#%%
clf.predict(X_test)

#%%
X_train_df = pd.DataFrame(X_train, columns = [features_df.columns])
feature_list = list(zip(X_train_df, clf.feature_importances_))

feature_df = pd.DataFrame(feature_list, columns = ["Features", "Feature_importance"])

#%%
# This displays the importance of different features
feature_df.sort(['Feature_importance'], ascending = False)

#%%
# 10-Fold Cross Validation -- we randomly particioned the training data into 10 equal size subsamples

print np.mean(cross_val_score(clf, X_train, y_train, cv = 10))

#%%
#predicted = cross_val_predict(clf, X_test, y_test, cv = 10)
#metrics.accuracy_score(y_test, X_test)
