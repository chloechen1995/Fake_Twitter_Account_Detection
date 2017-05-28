#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 15:11:59 2017

@author: Chloechen
"""

"""
Create a csv file that stores twitter_ids that do not get tweet information using the tweet.py due to the API Restriction

"""
#%%
import pandas as pd
import os
import glob

os.chdir("/Users/Chloechen/Desktop/tweet_analysis/")
final_data_id = pd.read_csv(open('final_data.csv', 'rU'), encoding = 'utf-8', usecols = ['id'])

total_id = final_data_id['id'].tolist()
total_id = map(str, total_id)

path_list = ['/Users/Chloechen/Desktop/Data/Tweet_' + str(i) for i in range(23)]

twitter_list = []
for path in path_list:
    os.chdir(path)
    files = glob.glob('*.csv')
    for file_name in files:
        basename = os.path.splitext(file_name)
        twitter_list.append(basename[0].split('_')[0]) 

left_id = list(set(total_id) - set(twitter_list))
left_id_df = pd.DataFrame(left_id, columns = ['id'])

os.chdir("/Users/Chloechen/Desktop/tweet_analysis/")
left_id_df.to_csv("left_id.csv", sep=',')