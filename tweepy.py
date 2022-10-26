#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 10:57:26 2020

@author: ebukaokpala
"""
import time
import tweepy
import os
from pathlib import Path
import json

consumer_key = 'NyYcEqPt5qDGt0L5ColGwe0RW'
consumer_secret = 'UDPLdRvNmIsanTklc3SSU1JOlpeuRDwkwcpEaASDhhNiSFwi1t'
access_token = '1277635861564153856-A2o6EeyBPeBN6vZxBqRqBxonWrzJfI'
access_token_secret = 'u0Fgk7EB0czmtKaiK8c0hNCCTZR0SAm0tlhv9RmpcBJNX'

file_path = "."

KEY_WORDS = ['coronavirus','COVID19','chinavirus','kungflu']

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        time = str(status.created_at)
        time = time.split(':')[0]
        time = time.split(' ')
        time = time[0] + "-" + time[-1]
        save_data(status._json,time)

    
file_object = None
file_name = None
path = None

def save_data(tweet,time):
    global file_object, file_name, folder, path
    if file_object is None:
        file_name = time
        folder = time[:7]
        path = os.path.join(file_path, folder)
        path_object = Path(path)
        if not path_object.exists():
            os.mkdir(path)
        file_object = open(path+'/covid19-'+file_name+'.jsonl','a')
        json.dump(tweet, file_object)
        file_object.write('\n')
        return
    if time[:7] != folder:
        file_object.close()
        file_name = time
        folder = time[:7]
        path = os.path.join(file_path, folder)
        path_object = Path(path)
        if not path_object.exists():
            os.mkdir(path)
        file_object = open(path+'/covid19-'+file_name+'.jsonl','a')
        json.dump(tweet, file_object)
        file_object.write('\n')
    else:
        if time != file_name:
            file_object.close()
            file_name = time
        file_object = open(path+'/covid19-'+file_name+'.jsonl','a')
        json.dump(tweet, file_object)
        file_object.write('\n')
    

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
    my_stream.filter(track=KEY_WORDS, languages=['en'])

if __name__ == "__main__":
    """Not handling retweets and quotes yet. Ask about this"""
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
