#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 23:29:42 2017

@author: Rachel
"""
# Get Followers/Following Data
import os
#os.chdir('/Users/Rachel/Desktop/STA 160')
#%%
import pandas as pd
import tweepy
import requests_cache
requests_cache.install_cache('fo1_cache')

#%%
import logging as log
log.basicConfig(filename = "fo1_log.txt", level = log.INFO, format='%(asctime)s %(message)s')
#%%
# read in data
all_ids = pd.read_csv('genuine.csv', index_col = 0)
all_ids = all_ids.id[:1000]

#%% ---------- Twitter API Setup
key = pd.read_table('key_tk.txt', header = None)
CONSUMER_KEY = key.iloc[0, 0]
CONSUMER_SECRET = key.iloc[1, 0]
ACCESS_TOKEN = key.iloc[2, 0]
ACCESS_TOKEN_SECRET = key.iloc[3, 0]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

#%% ---------- Get Followers/Followings id
def id_lists(user_id):
    try:
        path = os.getcwd() + '/fos_list'
        followers = pd.DataFrame(api.followers_ids(id = user_id))
        filename1 = str(user_id) + '_followers.csv'
        followers.to_csv(os.path.join(path,filename1))
        followings = pd.DataFrame(api.friends_ids(id = user_id))
        filename2 = str(user_id) + '_followings.csv'
        followings.to_csv(os.path.join(path,filename2)) 
        
    except tweepy.TweepError:
        pass
#%%
for i, id in enumerate(all_ids.id):
    id_lists(id)
    if (i % 100 == 0):
        info = str(i) + ' Succeed'
        log.info(info)
