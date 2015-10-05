from flask import Flask
from flask.ext.testing import TestCase
from eventserve.app import app as mainapp
import json
import requests

class EventServeTestCase(TestCase):
    @staticmethod
    def clear_test_es_index():
        # TODO: use api
        requests.delete('http://localhost:9200/test/event/_query',
            data=json.dumps({"query": { "match_all": {}}}))

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        super(EventServeTestCase, self).setUp()
        self.client = mainapp.test_client(self)
        self.clear_test_es_index()

    def post_json(self, uri, body_dict):
        return self.client.post(uri, headers={'Content-Type': 'application/json'},
                                data=json.dumps(body_dict))

    def get_json(self, uri):
        response = self.client.get(uri)
        return response, json.loads(response.data)

