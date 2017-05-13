#!/usr/bin/env python2.7

import pandas as pd
import glob
from api import *
import unicodecsv as csv
import logging as log
import requests_cache
requests_cache.install_cache('demo_cache')
import time

final_data = pd.read_csv(open('final data.csv', 'rU'), 
                      encoding = 'utf-8', usecols = ['id'])

# create a list of user ids
id_list = list(final_data['id'])

id_list.sort()

# Use reference: https://gist.github.com/yanofsky/5436496#file-tweet_dumper-py

def get_all_tweets(twitter_id):
    all_tweets = []
    tweets = api.user_timeline(user_id = twitter_id,count = 200)
    all_tweets.extend(tweets)
    oldest = all_tweets[-1].id - 1
    while len(tweets) > 0:
        tweets = api.user_timeline(user_id = twitter_id,count = 200, max_id = oldest)
        all_tweets.extend(tweets)
        oldest = all_tweets[-1].id - 1
    outtweets = [[tweet.id_str, tweet.created_at, tweet.source, tweet.favorite_count, tweet.retweet_count, tweet.text.encode("utf-8")] for tweet in all_tweets]
    tweets = [tweets + [twitter_id] for tweets in outtweets]
    with open('%s_tweets.csv' % twitter_id, 'wb') as f:
        writer = csv.writer(f, encoding='utf-8')
        writer.writerow(["id","created_at", "source", "favorite_count", "retweet_count", "tweet_text", "id"])
        writer.writerows(tweets)
    
    pass

for i, user_id in enumerate(id_list):
    try:
        get_all_tweets(user_id)
        if ((i+1) % 100 == 0):
            log.basicConfig(filename = "my_log.txt", level = log.INFO)
            log.info("Reaches to the goal")
    except tweepy.TweepError as error:
                    continue
