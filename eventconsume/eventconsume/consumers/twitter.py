#!/usr/bin/env python
import yaml
import tweepy
import pprint
import sys
import logging
import os.path

from eventconsume.exceptions import ConsumerAccessDenied
from eventconsume.consumer import Consumer
from eventconsume.models import Event, ConsumerError

logger = logging.getLogger()

class TwitterStreamListener(tweepy.StreamListener):
    """
    Stream listener subclass for twitter API event handling.
    """
    def __init__(self, api, success_callback, error_callback):
        super(TwitterStreamListener, self).__init__(api)
        self.api = api
        self.success_callback = success_callback
        self.error_callback = error_callback

    def on_status(self, status):
        if status.geo or status.coordinates:
            # normalize it into a model instance and pass it onto the success callback
            
            # twitter API has deprecated the 'geo' field but coordinates gives us lon,lat instead
            # of lat,lon, so reverse it
            lon, lat = status.coordinates['coordinates']
            event = Event(text=status.text, location=(lat, lon), creator=status.author.screen_name, site='twitter')
            self.success_callback(event)

            #print 'Text:', status.text
            #print 'Geo:', status.geo
            #print 'Coordinates:', status.coordinates
            #print 'Author:', status.author.screen_name
            #print '*' * 50

    def on_error(self, status_code):
        self.error_callback(ConsumerError('HTTP error occurred',  status_code))

    def on_exception(self, exception):
        self.error_callback(ConsumerError('Unexpected exception occurred', exception))

    def on_limit(self, track):
        self.error_callback(ConsumerError('Rate limit exceeded', track))

    def on_timeout(self):
        self.error_callback(ConsumerError('Stream timed out'))
    
    def on_disconnect(self, notice):
        self.error_callback(ConsumerError('Stream issued a disconnect notice', notice))


class TwitterConsumer(Consumer):
    def __init__(self):
        self.config = self._load_config()

        try:
            self.consumer_key = self.config['consumer_key']
            self.consumer_secret = self.config['consumer_secret']
            self.access_token = self.config['access_token']
            self.access_token_secret = self.config['access_token_secret']
        except KeyError as exc:
            raise KeyError('Invalid configuration for TwitterConsumer: ' + unicode(exc))

        self.api = None    # our authenticated twitter (tweepy) api
        self.stream = None # the stream for this twitter api
        self.auth = None   # twitter authentication credentials

    def _load_config(self):
        try:
            base, fname = os.path.split(os.path.realpath(__file__))
            fname = os.path.splitext(fname)[0] + '.yml'
            with open(os.path.join(base, fname)) as config_file:
                config = yaml.load(config_file.read())
        except (IOError, ValueError) as exc:
            raise # for now

        return config
        
    def connect(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)

        try:
            self.api.verify_credentials()
        except tweepy.TweepError as exc:
            raise ConsumerAccessDenied('Error occurred while verifying API credentials: ' + str(exc))


    def start(self, success_callback, error_callback):
        listener = TwitterStreamListener(self.api, success_callback, error_callback)
        self.stream = tweepy.Stream(self.auth, listener)
        self.stream.sample()

    def stop(self):
        self.stream.disconnect()

