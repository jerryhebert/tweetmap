from flask import Flask, redirect, request, jsonify, abort

from eventserve.docindex import DocIndex

app = Flask(__name__)

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

    index = DocIndex()
    raw_hits = index.search(tags.split(), lat, lon, distance)
    return jsonify({
        "hits": [hit['_source'] for hit in raw_hits.get('hits', {}).get('hits', [])],
        "total": raw_hits['hits']['total']
    })

app.debug = True
app.run()


