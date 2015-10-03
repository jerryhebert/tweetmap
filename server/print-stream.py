#!/usr/bin/env python
import yaml
import tweepy
import pprint
import sys

try:
    config = yaml.load(open('etc/config.yml').read())
except (IOError, ValueError) as exc:
    print 'Config missing or invalid:', str(exc)
    sys.exit(1)

auth = tweepy.OAuthHandler(config.get('twitter_consumer_key'), config.get('twitter_consumer_secret'))
auth.set_access_token(config.get('twitter_access_token'), config.get('twitter_access_token_secret'))


api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.geo or status.coordinates:
            print 'Text:', status.text
            print 'Geo:', status.geo
            print 'Coordinates:', status.coordinates
            print 'Author:', status.author.screen_name
            print '*' * 50

stream = tweepy.Stream(auth, StreamListener(api))
stream.sample()


