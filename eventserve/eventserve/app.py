import elasticsearch
from flask import Flask, redirect, request, jsonify, abort


app = Flask(__name__)

es = elasticsearch.client.Elasticsearch()

def geocell_query(page_from, page_size, distance, lat, lon, tags):
    tag_matches = [{ "match": { "message": tag } } for tag in tags]

    return {
        "from": page_from,
        "size": page_size,
        "query": {
            "filtered": {
                "query": {
                    "bool": {
                        "must": tag_matches
                    }
                },
                "filter": {
                    "geohash_cell": {
                        "_cache": True,
                        "precision": distance,
                        "location": {
                            "lat":  lat,
                            "lon": lon
                        }
                    }
                }
            }
        },
        "sort": {
            "timestamp": {
                "order": "desc"
            }
        }
    }

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
    tags = request.args.get('tags', [])

    if not lat or not lon:
        abort(400, 'Must specify both `lat` and `lon`')

    query = geocell_query(page_from, page_size, distance, lat, lon, tags.split())
    raw_hits = es.search(index='events', doc_type='event', body=query)

    return jsonify({
        "hits": [hit['_source'] for hit in raw_hits.get('hits', {}).get('hits', [])],
        "total": raw_hits['hits']['total']
    })

app.debug = True
app.run()


