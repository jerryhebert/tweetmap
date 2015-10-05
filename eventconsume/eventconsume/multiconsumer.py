import requests
import logging
import json

from eventconsume.consumers.twitter import TwitterConsumer
from consumer import Consumer

class MultiConsumer(Consumer):
    """
    Multiconsumer class to manage multiple event consumers firing.
    
    TODO/BUG: current implementation does not actually run them all, it only supports one.
    """
    def __init__(self, consumers):
        self.all_consumers = {c(): {'alive': True, 'class': c} for c in consumers}

    @property
    def consumers(self):
        return [c for c in self.all_consumers if self.all_consumers[c]['alive']]

    def remove(self, consumer):
        self.all_consumers[consumer]['alive'] = False

    def start(self):
        for consumer in self.consumers:
            try:
                # TODO/BUG: Make this into a greenlet or a twisted deferred or something
                # so that this code actually does what it's supposed to. Right now it will
                # just block which is semi-ok for a demo but obviously not good if we ever
                # have more event gennerators to consume
                consumer.start(self._on_success, self._on_failure)
            except Exception as exc:
                logging.error("Failed to start consumer, marking as dead: " + str(exc))
                self.remove(consumer)
                

    def connect(self):
        for consumer in self.consumers:
            try:
                consumer.connect()
            except Exception as exc:
                logging.error("Failed to connect consumer, marking as dead: " + str(exc))
                self.remove(consumer)

    def stop(self):
        for consumer in self.consumers:
            try:
                consumer.stop()
            except Exception:
                pass # squelch this since we're killing them anyway

    @staticmethod
    def _on_success(event):
        body = {
            'message': event.message,
            'creator': event.creator,
            'location': event.location,
            'site': event.site,
            'timestamp': event.timestamp
        }
        response = requests.post('http://localhost:5000/events', data=json.dumps(body),
                                 headers={'Content-Type': 'application/json'})

    @staticmethod
    def _on_failure(context):
        logging.error('Failure occurred while consuming: ' + str(context))


