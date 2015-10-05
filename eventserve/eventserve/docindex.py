import elasticsearch

class GeoCell(object):
    """
    Object to represent a particular geocell for use in geocell-based filtering
    """
    def __init__(self, lat, lon, radius):
        self.lat = lat
        self.lon = lon
        self.radius = radius


class PageInfo(object):
    """
    Represents query paging information.
    """
    def __init__(self, page_from=0, page_size=20):
        self.start = page_from                
        self.size  = page_size


class DocIndex(object):
    """
    An index to store our documents. Currently only supports
    Elasticsearch but from here we could consider wiring in
    other index types.
    """
    def __init__(self, index='events', doc_type='event'):
        self.index_name = index
        self.doc_type = doc_type
        self.es = elasticsearch.client.Elasticsearch()

    def search(self, tags, geocell=None, page_info=None):
        if not page_info:
            page_info = PageInfo()
        query = self._query_dsl(tags, geocell)
        return self.es.search(index='events', doc_type='event', body=query,
                              from_=page_info.start, size=page_info.size)

    @staticmethod
    def _query_dsl(tags, geocell):
        tag_matches = [{ "match": { "message": tag } } for tag in tags]

        base_query = {
            "query": {
                "filtered": {
                }
            },
            "sort": {
                "timestamp": {
                    "order": "desc"
                }
            }
        }

        if tag_matches:
            base_query['query']['filtered']['query'] = {
                "bool": {
                    "must": tag_matches
                }
            }
        if geocell:
            base_query['query']['filtered']['filter'] = {
                "geo_distance": {
                    "_cache": True,
                    "distance": geocell.radius,
                    "distance_type": "plane",
                    "location": {
                        "lat":  geocell.lat,
                        "lon": geocell.lon
                    }
                }
            }

            # geohash cell produces incorrect results for reasons I don't understand
            """
            base_query['query']['filtered']['filter'] = {
                "geohash_cell": {
                    "_cache": True,
                    "precision": geocell.radius,
                    "location": {
                        "lat":  geocell.lat,
                        "lon": geocell.lon
                    }
                }
            }
            """

            return base_query

    def index(self, message, creator, location, site, timestamp, ttl=60*60*24*7):
        self.es.index(self.index_name, self.doc_type, ttl=ttl, body={
            'message': message,
            'creator': creator,
            'location': location,
            'site': site,
            'timestamp': timestamp
        })

