"""
Loads all consumer plugins and sets up promises for each of them
such that whenever we have an event ready, the reactor can handle
this with the appropriate event persistence call.
"""

# but in reality, right now we just hardcode twitter!
from eventconsume.consumers.twitter import TwitterConsumer
import elasticsearch

def get_ttl_from_config():
    # fake it for now
    one_week = 60*60*24*7 
    return one_week

es = elasticsearch.client.Elasticsearch()
def success(event):
    es.index(index='events', doc_type='event', ttl=get_ttl_from_config(), body={
        'message': event.message,
        'creator': event.creator,
        'location': event.location,
        'site': event.site,
        'timestamp': event.timestamp
    })

def failure(error):
    print error

t = TwitterConsumer()
t.connect()
t.start(success, failure)

