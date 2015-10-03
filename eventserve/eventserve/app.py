import elasticsearch
from flask import Flask, redirect, request, jsonify

def get_host_from_config():
    return '172.31.25.207'

app = Flask(__name__)
es = elasticsearch.client.Elasticsearch()

@app.route('/')
def root():
    return redirect('/events', 302)

@app.route('/events')
def events():
    return jsonify(es.search(index='events', doc_type='event'))

app.run(host=get_host_from_config())

