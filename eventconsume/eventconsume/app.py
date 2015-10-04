"""
Loads all consumer plugins and sets up promises for each of them
such that whenever we have an event ready, the reactor can handle
this with the appropriate event persistence call.
"""

# but in reality, right now we just hardcode twitter!
import requests
import json
from eventconsume.consumers.twitter import TwitterConsumer

def success(event):
    body = {
        'message': event.message,
        'creator': event.creator,
        'location': event.location,
        'site': event.site,
        'timestamp': event.timestamp
    }
    response = requests.post('http://localhost:5000/events', data=json.dumps(body),
                             headers={'Content-Type': 'application/json'})

def failure(error):
    print error

t = TwitterConsumer()
t.connect()
t.start(success, failure)

