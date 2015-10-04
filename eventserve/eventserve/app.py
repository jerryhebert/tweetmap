import elasticsearch
from flask import Flask, redirect, request, jsonify, abort

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Api
from flask.ext.restful.representations.json import output_json
output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}

app = Flask(__name__)

es = elasticsearch.client.Elasticsearch()

query_template = """
{
  "from": %d,
  "size": %d,
  "query": {
    "filtered": {
      "filter": {
        "geohash_cell": {
          "_cache": true,
          "precision": "%s",
          "location": {
            "lat":  %f,
            "lon": %f
          }
        }
      }
    }
  },
  "sort": { "timestamp": { "order": "desc" } }
}
"""

@app.route('/')
def root():
    return redirect('/events', 302)

@app.route('/events')
def events():
    page_from = request.args.get('from', 0)
    page_size = request.args.get('size', 250)
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    distance = request.args.get('distance', '10km')

    if not lat or not lon:
        abort(400, 'Must specify both `lat` and `lon`')

    query = query_template % (int(page_from), int(page_size), distance,
                              float(lat), float(lon))
    raw_hits = es.search(index='events', doc_type='event', body=query)

    return jsonify({
        "hits": [hit['_source'] for hit in raw_hits.get('hits', {}).get('hits', [])],
        "total": raw_hits['hits']['total']
    })

app.debug = True
app.run()


