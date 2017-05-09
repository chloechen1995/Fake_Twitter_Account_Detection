#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 17:04:20 2017

@author: Rachel
"""
#%%
import os
os.getcwd()
#os.chdir('./Desktop/STA 160')
os.chdir('/home/tongkewu/STA160/network')

#%%
import pandas as pd
import tweepy
import numpy as np
# FIXME: Add logging to keep track of what's happening:
#
#   import logging as log
#
#   # Only messages at or above the log level are printed. The order is:
#   #
#   #   DEBUG < INFO < WARNING < ERROR < CRITICAL
#   #
#   log.basicConfig(filename = "my_log.txt", level = log.INFO)
#
#   # Print an info message.
#   log.info("This is some info!")
#

#%% ---------- Set up API
CONSUMER_KEY = 'QifrSmYAQ2mjIf8kiPoL2kI4v'
CONSUMER_SECRET = 'qHXPmXDd4Gw2cqZ5zKmDpU6drKEHTF396pj9qyoUYWDcLsFOlm'
ACCESS_TOKEN = '3379234805-hUmhUJa0oV9V1mnKDuB6bitJ1QTEjdq2c9zE0RA'
ACCESS_TOKEN_SECRET = 'cQiqDWDuoLj8SH68d6JuPhthToImk3WzmcQ3pbyxYfYK1'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

#%% ---------- Read In Data
# load in genuine accounts data
all_ids = pd.read_csv('all_ids.csv', index_col = 0)

test_ids = all_ids.sample(n=2)

#%% ---------- Neighbor-based Features
# - Average number of followers of a user's followings
avg_nbs_fos = {}
# - Average number of tweets of a user's followings
avg_nbs_tws = {}
# - Followings to median neighbors’ followers
fo_med = {}
for i, user_id in enumerate(all_ids.id):
    try:
        followings = api.friends_ids(id = user_id)
    except tweepy.TweepError:
        pass
    
    stat1 = []
    stat2 = []
    for following in followings:
        try:
            user = api.get_user(id =  following)
            stat1.append(user.followers_count)
            stat2.append(user.statuses_count)
        except tweepy.TweepError:
            pass
    avg_nbs_fos[user_id] = np.mean(stat1)
    
    avg_nbs_tws[user_id] = np.mean(stat2)
    
    fo_med[user_id] = len(followings) / np.median(stat1)

    # FIXME:
    #if (i % 1000 == 0):
    #    # Print to log
    #    # Write to a file (CSV, etc)

#%% 
df1 = pd.DataFrame.from_dict(avg_nbs_fos, orient = 'index') 
df1.columns = ['avg_nbs_fos']
df2 = pd.DataFrame.from_dict(avg_nbs_tws, orient = 'index') 
df2.columns = ['avg_nbs_tws']
df3 = pd.DataFrame.from_dict(fo_med, orient = 'index') 
df3.columns = ['fo_med']

final = df1.merge(df2, left_index = True, right_index = True).merge(df3, left_index = True, right_index = True)
final.to_csv('Neighbor_Based_Features.csv')
