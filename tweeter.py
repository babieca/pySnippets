#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import time
import re
from terminaltables import SingleTable

API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = '4061156243-'
ACCESS_TOKEN_SECRET = ''


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

tweet_search = ''
tweet_filter = ' -filter:retweets'


query = tweet_search + tweet_filter
max_tweets = 10

searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

filt = '[^A-Za-z0-9\ \/\\\:\.\,\[\]\!\-\_\{\}\$\£\€\%\+\=\&\^\*\#\@\?\<\>\;\~]+'

count = 0
table_data = [['#','Date', 'Username', 'Lang', 'retweeted', 'truncated', 'Tweet']]
for tweet in searched_tweets:
    if (not tweet.retweeted) and ('RT @' not in tweet.text):
        table_data.append([
                str(count),
                tweet.created_at,
                re.sub(filt, '', tweet.user.name),
                tweet.lang,
                'Yes' if tweet.retweeted else 'No',
                'Yes' if tweet.truncated else 'No',
                re.sub(filt, '', tweet.text.encode("ascii",errors="ignore").decode("ascii"))
                ])
        count +=1

table = SingleTable(table_data)

limits = api.rate_limit_status
try:
    limits = api.rate_limit_status()
    #for usertime line api limits -- typicaly 150 hits per 15mins
    usertimeline_remain = limits['resources']['statuses']['/statuses/user_timeline']['remaining']
    usertimeline_limit = limits['resources']['statuses']['/statuses/user_timeline']['limit']
    usertimeline_time = limits['resources']['statuses']['/statuses/user_timeline']['reset']
    usertimeline_time_local = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(usertimeline_time))
    print('Twitter API: remain: %s / limit: %s - reseting at: %s' %(usertimeline_remain, usertimeline_limit, usertimeline_time_local))
    print('response: %s' % (getattr(api, 'last_response', None))) #just get the response, 429 = rate limit exceeded / https://dev.twitter.com/overview/api/response-codes

except:
    print('nope couldn\'t get them')
    print('response: %s' % (getattr(api, 'last_response', None))) #just get the response, 429 = rate limit exceeded / https://dev.twitter.com/overview/api/response-codes
    print(limits)
    
print table.table
