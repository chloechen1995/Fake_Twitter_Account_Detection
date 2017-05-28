#!/usr/bin/env python2.7

import pandas as pd
import glob
from api import *
import unicodecsv as csv
import logging as log
import requests_cache
requests_cache.install_cache('demo_cache')
import time
import sys

"""
get tweets for the leftover twitter_ids from API
"""

left_data = pd.read_csv(open('left_id.csv', 'rU'), 
                      encoding = 'utf-8', usecols = ['id'])
id_list = list(left_data['id'])

id_list.sort()

id_list_split = [id_list[i:i + 500] for i in xrange(0, len(id_list), 500)]

# Use reference: https://gist.github.com/yanofsky/5436496#file-tweet_dumper-py

def get_all_tweets(twitter_id):
    all_tweets = []
    tweets = api.user_timeline(user_id = twitter_id,count = 200)
    all_tweets.extend(tweets)
    if len(all_tweets) > 0:
        oldest = all_tweets[-1].id - 1
        while len(tweets) > 0:
            tweets = api.user_timeline(user_id = twitter_id,count = 200, max_id = oldest)
            all_tweets.extend(tweets)
            oldest = all_tweets[-1].id - 1
        outtweets = [[tweet.id_str, tweet.created_at, tweet.source, tweet.favorite_count, tweet.retweet_count, tweet.text.encode("utf-8")] for tweet in all_tweets]
        tweets = [tweets + [twitter_id] for tweets in outtweets]
        with open('%s_tweets.csv' % twitter_id, 'wb') as f:
            writer = csv.writer(f, encoding='utf-8')
            writer.writerow(["tweet_id","created_at", "source", "favorite_count", "retweet_count", "tweet_text", "user_id"])
            writer.writerows(tweets)

        pass

input_1 = int(sys.argv[1])
for i, user_id in enumerate(id_list_split[input_1]):
    try:
        get_all_tweets(user_id)
        if ((i+1) % 100 == 0):
            log.basicConfig(filename = "my_log.txt", level = log.INFO)
            log.info("Reaches to the goal")
    except tweepy.TweepError as error:        
        if error[0][0] == 'Rate limit exceeded':
                time.sleep(15 * 60 + 15)
                continue
