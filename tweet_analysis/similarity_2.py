#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 10:37:33 2017

@author: Chloechen
"""

#%%
from __future__ import division
"""
This script calculates tweet similarity ratio 2 
"""
#%%
from textblob import TextBlob
import pandas as pd
from nltk.corpus import stopwords
from math import factorial
import itertools as it
from numpy import linalg as LA

#%%
def modify_df(user_tweets):
    """
    remove unnecessary words from the user_tweets.csv
    
    Argument: user_tweets
    
    Return: user_tweets dataframe
    """

    special_remove = [str(tweets).decode('utf-8').encode('ascii','ignore') for tweets in user_tweets['Tweet_Text']] 
    user_tweets['tweet_split'] = [tweets.lower().split() for tweets in special_remove]
    user_tweets['tweet_split'] = [filter(lambda x: not (x.startswith("@") or x.startswith("#") or x.startswith("https:") or x in stopwords.words("english") or x.startswith("rt") or x[0].isdigit()), tweet) for tweet in user_tweets['tweet_split']]
    user_tweets['tweet_split_string'] = [' '.join(str(x) for x in tweets) for tweets in user_tweets['tweet_split']]
    return user_tweets

#%%
def comb_2(user_tweets):
    """
    calculate the number of tweet combinations
    
    Argument: user_tweets
    
    Return: total number of tweet combinations
    """
    num_tweets = len(user_tweets['Tweet_Text'])
    return int(factorial(num_tweets) / (factorial(2) * factorial(num_tweets - 2)))

#%%
def sim_formula(user_tweets):
    """
    calculate set of pair in tweets
    
    Argument: user_tweets
    
    Return: set of pair in tweets ratio
    """
    if len(user_tweets) != 0: 
        user_tweets = modify_df(user_tweets)
        ind = [TextBlob(tweets).word_counts for tweets in user_tweets['tweet_split_string']]
        vector_df = pd.DataFrame(ind)
        vector_df = vector_df.fillna(0)
        vector_matrix = vector_df.as_matrix()
        idx = list(it.combinations(range(vector_df.shape[0]), 2))
        sim_dot = {}
        for i, j in idx:
            sim_dot[(i, j)] = vector_matrix[i, :].dot(vector_matrix[j,:])

        sim_norm = {}
        for x, y in idx:
            sim_norm[(x, y)] = LA.norm(vector_matrix[x, :]) * LA.norm(vector_matrix[y,:])
        
        dot_set = set(sim_dot)
        norm_set = set(sim_norm)

        sim_result = {}
        for key in dot_set.intersection(norm_set):
            if sim_norm[key] != 0:
                sim_result[key] = (sim_dot[key] / sim_norm[key])/comb_2(user_tweets)
        result_sum = sum(sim_result.itervalues())
    else:
        result_sum = "None"

    return result_sum
