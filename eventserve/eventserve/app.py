"""
Basic web server to serve events for our app.
"""

from flask import Flask, redirect, request, jsonify, abort
from eventserve.docindex import DocIndex, GeoCell, PageInfo

app = Flask(__name__)

@app.route('/')
def root():
    return redirect('/events', 302)

@app.route('/events', methods=['GET'])
def get_events():
    """
    Fetches all events matching the query parameters. Parameters are:
        from: the start object of the page
        size: the size of the page we request
        lat: the latitude of our geocell
        lon: the longitude of our geocell
        tags: tags to filter by
    """
    page_from = request.args.get('from', 0)
    page_size = request.args.get('size', 20)
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    distance = request.args.get('distance', '10km')
    tags = request.args.get('tags', [])
    if tags:
        tags = tags.split()

    if not lat or not lon:
        abort(400, 'Must specify both `lat` and `lon`')

    index = DocIndex()
    raw_hits = index.search(tags, GeoCell(lat, lon, distance), PageInfo(page_from, page_size))
    return jsonify({
        "hits": [hit['_source'] for hit in raw_hits.get('hits', {}).get('hits', [])],
        "total": raw_hits['hits']['total']
    })

@app.route('/events', methods=['POST'])
def create_event():
    """
    Indexes a new event with the given data. All fields are required:
        message
        creator
        location
        site
        timestamp
    """
    required_fields = 'message', 'creator', 'location', 'site', 'timestamp'

    for field in required_fields:
        if request.json.get(field) is None:
            abort(400, "Missing required field: " + field)

    index = DocIndex()
    index.index(*[request.json[field] for field in required_fields])
    return 'ok'

app.run(use_reloader=False)

