#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 00:28:34 2017

@author: Chloechen
"""

"""
analyze tweet‘s authenticity using url_ratio, url_unique_ratio, hashtag_ratio, username_ratio and username_unique_ratio
"""

from __future__ import division
import pandas as pd
from compiler.ast import flatten
import re

def url_ratio(user_id):
    """
    calculate the percentage of 20 recent Tweets containing URLs
    
    Argument: tweets_df
    
    Return: tweets_url_ratio
    """
    user_tweets = pd.read_csv(str(user_id) + "_tweets_.csv")
    top_20 = user_tweets[:20]
    tweets_url_ratio = sum(top_20['Tweet_Text'].str.contains("https:") == True)/len(user_tweets['Tweet_Text'])
    return tweets_url_ratio


def url_unique_ratio(user_id):
    """
    calculate the ratio of the number of unique URLs in the 20 recent tweets
    
    Argument: tweets_df
    
    Return: url_ratio
    """
    user_tweets = pd.read_csv(str(user_id) + "_tweets_.csv")
    top_20 = user_tweets[:20]
    # find all the urls using regular expression
    urls = [re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweets) for tweets in top_20['Tweet_Text']]
    # flatten a list of lists
    urls_flatten = flatten(urls)
    # get the first two parts of the url
    urls_split = [u.split('/')[0:3] for u in urls_flatten]
    
    urls_unique = [list(u) for u in set(tuple(u) for u in urls_split)]
    url_unique= len(urls_unique)
    tweet_total = len(user_tweets['Tweet_Text'])
    url_ratio = url_unique/tweet_total
    return url_ratio

def hashtag_ratio(user_id):
    """
    calculate the hashtag ratio
    
    Argument: tweets_df
    
    Return: hashtag ratio
    """
    user_tweets = pd.read_csv(str(user_id) + "_tweets_.csv")
    top_20 = user_tweets[:20]
    hashtag_ratio = sum(top_20['Tweet_Text'].str.contains("#"))/len(top_20['Tweet_Text'])
    return hashtag_ratio
    
def username_ratio(user_id):
    """
    calculate the username ratio
    
    Argument: tweets_df
    
    Return: username ratio
    """
    user_tweets = pd.read_csv(str(user_id) + "_tweets_.csv")
    top_20 = user_tweets[:20]
    username_ratio = sum(top_20['Tweet_Text'].str.contains("@"))/len(top_20['Tweet_Text'])
    return username_ratio
    
def username_unique_ratio(user_id):
    """
    calculate the ratio of the number of unique @usernames
    
    Argument: tweets_df
    
    Return: username_unique_ratio
    """
    user_tweets = pd.read_csv(str(user_id) + "_tweets_.csv")
    top_20 = user_tweets[:20]
    username = [re.findall('@([A-Za-z0-9_]+)', tweets) for tweets in top_20['Tweet_Text']]
    # flatten a list of lists
    username_flatten = flatten(username)
    username_unique = set(username_flatten)
    user_unique= len(username_unique)
    # total number of users that were being @, not all the tweets
    tweet_total = len(user_tweets['Tweet_Text'])
    user_ratio = user_unique/tweet_total
    return user_ratio



