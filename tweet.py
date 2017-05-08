#!/usr/bin/env python2.7

import pandas as pd
import glob
from api import *
import unicodecsv as csv

# read all the files
genuine = pd.read_csv(open('User dataset/genuine account.csv', 'rU'), 
                      encoding = 'utf-8', usecols = ['id'] )

# load in fake accounts data
path =r'./User dataset/fake data/'
allFiles = glob.glob(path + "/*.csv")
fake = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(open(file_, 'rU'), encoding = 'utf-8', usecols = ['id'])
    list_.append(df)
fake = pd.concat(list_)
# merge all the data 
all_ids = pd.concat([genuine, fake])

# create a list of user ids
id_list = list(all_ids['id'])
id_list = [str(i) for i in id_list]
items = ["False", "None", "nan"]
id_list = filter(lambda x: x not in items, id_list)
final_id_list = [int(i) for i in id_list]

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


for i in final_id_list:
    try:
        get_all_tweets(i)
    except tweepy.TweepError as error:
        pass
