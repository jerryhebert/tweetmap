from flask import Flask, url_for
from flask.ext.testing import TestCase
import unittest
from eventserve.docindex import DocIndex, GeoCell
from utils import EventServeTestCase
import json
import random
import time

class EventsApiTestCase(EventServeTestCase):
    @staticmethod
    def flush_es_index():
        # There is some latency here before ES finishes indexing a document.
        # in order to prove it's there, I'm going to break the law slightly.
        # The ES index supposedly refreshes every second but there is probably
        # a way to manually flush it.
        time.sleep(1)

    @staticmethod
    def degree_compare(d1, d2, e=0.0001):
        if abs(d1 - d2) <= e:
            return True
        else:
            return False

    @staticmethod
    def random_lng():
        return random.random() * 180 * [1, -1][random.randint(0, 1)]

    @staticmethod
    def random_lat():
        return random.random() * 90 * [1, -1][random.randint(0, 1)]

    def create_test_event(self, location=None, message='#foo is cooler than #bar',
                          timestamp=123456789, creator='joe', site='twitter'):
        if location is None:
            location = [self.random_lng(), self.random_lat()]

        return self.post_json('/events', {
            'location': location,
            'message': message,
            'timestamp': timestamp,
            'creator': creator,
            'site': 'twitter'
        })
            
    def test_post_of_valid_data_succeeds(self):
        response = self.create_test_event()
        self.assertEquals(response.status_code, 200)

    def test_post_of_invalid_data_does_not_succeed(self):
        response = self.post_json('/events', { 'message': 'foo' })
        self.assertEquals(response.status_code, 400)

    def test_post_valid_data_should_be_indexed(self):
        _, before_data = self.get_json('/events?lat=777.777&lon=777.777&distance=1000km')

        response = self.create_test_event(location=[777.777, 777.777])
        self.assertEquals(response.status_code, 200)

        self.flush_es_index()

        after, after_data = self.get_json('/events?lat=777.777&lon=777.777&distance=1000km')
        self.assertEquals(before_data['total'] + 1, after_data['total'])
    
    def test_query_event_within_location_should_return_event(self):
        lat, lng = self.random_lat(), self.random_lng()
        event = self.create_test_event(location=[lng, lat])
        self.flush_es_index()
        index = DocIndex()
        result = index.search([], GeoCell(lat, lng, '1km'))
        
        self.assertTrue(result.get('hits', []))
        loc = result['hits']['hits'][0]['_source']['location']
        self.assertTrue(self.degree_compare(loc[0], lng))
        self.assertTrue(self.degree_compare(loc[1], lat))

    def test_query_event_within_location_should_not_return_event_outside_of_location(self):
        km2lat = 110.574 # roughly
        lat, lng = self.random_lat(), self.random_lng()
        event = self.create_test_event(location=[lng, lat])
        # now create another event, far away from it
        event = self.create_test_event(location=[lng, lat + 10/km2lat])

        self.flush_es_index()

        index = DocIndex()
        result = index.search([], GeoCell(lat, lng, '9km'))
        
        self.assertEquals(result['hits']['total'], 1)

    def test_hits_queried_by_tags_should_contain_tag(self):
        msg1 = 'what a horrible #night to have a #curse'
        msg2 = 'the morning #sun has vanquished the horrible #night'

        self.create_test_event(message=msg1)
        self.create_test_event(message=msg2)
        self.flush_es_index()

        index = DocIndex()
        result = index.search(['#curse'])
        hits = result['hits']['hits']
        self.assertEquals(len(hits), 1)
        self.assertEquals(hits[0]['_source']['message'], msg1)

        result = index.search(['#sun'])
        hits = result['hits']['hits']
        self.assertEquals(len(hits), 1)
        self.assertEquals(hits[0]['_source']['message'], msg2)

        result = index.search(['#night'])
        hits = result['hits']['hits']
        self.assertEquals(len(hits), 2)
        self.assertEquals(hits[0]['_source']['message'], msg2)
        self.assertEquals(hits[1]['_source']['message'], msg1)


    def test_hits_should_return_in_desc_order(self):
        self.create_test_event(message='first', timestamp=2222222222)
        self.create_test_event(message='second', timestamp=1111111111)
        self.create_test_event(message='third', timestamp=3333333333)
        self.flush_es_index()

        index = DocIndex()
        result = index.search([])
        hits = result['hits']['hits']
        self.assertEquals(len(hits), 3)

        hits = result['hits']['hits']
        self.assertEquals(hits[0]['_source']['message'], 'third')
        self.assertEquals(hits[1]['_source']['message'], 'first')
        self.assertEquals(hits[2]['_source']['message'], 'second')


