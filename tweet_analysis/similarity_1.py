#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 00:48:27 2017

@author: Chloechen
"""

"""
calculate tweet similarity
"""

#%%
import pandas as pd
from nltk.corpus import stopwords
import itertools as it
from math import factorial
import numpy as np
import os 

os.chdir('/Users/Chloechen/Desktop/Sample_Tweets')
#%%
def create_df(user_tweets):
    """
    remove unnecessary words from the user_tweets.csv
    
    Argument: user_id
    
    Return: user_tweets dataframe
    """
    #user_id = str(user_id)
    #user_tweets = pd.read_csv(user_id + "_tweets_.csv")
    special_remove = [str(tweets).decode('utf-8').encode('ascii','ignore') for tweets in user_tweets['Tweet_Text']] 
    user_tweets['tweet_split'] = [tweets.lower().split() for tweets in special_remove]
    user_tweets['tweet_split'] = [filter(lambda x: not (x.startswith("@") or x.startswith("#") or x.startswith("https:") or x in stopwords.words("english") or x.startswith("rt")), tweet) for tweet in user_tweets['tweet_split']]
    user_tweets['tweet_split_string'] = [' '.join(str(x) for x in tweets) for tweets in user_tweets['tweet_split']]
    return user_tweets
    

#%%
def cal_char(user_tweets):
    """
    calculate the length of tweets
    
    Argument: user_tweets dataframe created by create_df function
    
    Return: the length of every tweet
    """
    user_tweets['tweet_split'] = [str(tweets).lower().split() for tweets in user_tweets['Tweet_Text']]
    user_tweets['tweet_string'] = [filter(lambda x: not (x.startswith("@") or x.startswith("#") or x.startswith("https:") or x.startswith("rt")), tweet) for tweet in user_tweets['tweet_split']]
    char_count = [len(user_tweets['tweet_string'][i]) for i in range(len(user_tweets['tweet_string']))]
    return char_count

#%%
def comb_2(tweet_df):
    """
    calculate the number of tweet combinations
    
    Argument: num_tweets
    
    Return: total number of tweet combinations
    """
    num_tweets = len(tweet_df['Tweet_Text'])
    if num_tweets > 1:
        result = int(factorial(num_tweets) / (factorial(2) * factorial(num_tweets - 2)))
    else:
        result = 0
    return result

#%%
def tweet_set(tweet_df):
    """
    create a set of possible tweet-to-tweet combinations among any two tweets
    
    Argument: tweet_df
    
    Return: set of tweet combinations
    """
    tweet_list = list(tweet_df["tweet_split"])
    tweet_tuples = list(it.combinations(tweet_list, 2))
    tweet_df = pd.DataFrame(tweet_tuples, columns = ["tweet_1", "tweet_2"])
    tweet_df["tweet_combination"] = tweet_df["tweet_1"] + tweet_df["tweet_2"]
    tweet_df['common_words'] = [set([x for x in tweet if tweet.count(x) > 1]) for tweet in tweet_df['tweet_combination']]
    tweet_df['common_count'] = [len(tweet_df['common_words'][i]) for i in range(len(tweet_df['common_words']))]  
    return tweet_df

#%%
def tweet_sim(user_tweets):
    if len(user_tweets) != 0: 
	    user_tweets = create_df(user_tweets)
	    char_count = cal_char(user_tweets)
	    tweet_comb = tweet_set(user_tweets)
	    if comb_2(user_tweets) != 0:
	        sim_value = tweet_comb['common_count'].sum() / (np.mean(char_count) * comb_2(user_tweets))
	    else:
	        sim_value = 0
    else:
        sim_value = "None"
    return sim_value