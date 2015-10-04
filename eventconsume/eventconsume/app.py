"""
Loads all consumer plugins and sets up promises for each of them
such that whenever we have an event ready, the reactor can handle
this with the appropriate event persistence call.
"""

from multiconsumer import MultiConsumer

def load_consumer_plugins():
    """
    Ideally this should read all of the plugins in the right
    location and return those classes. For now, it's just a
    local import which returns the one consumer that we have.
    """
    from eventconsume.consumers.twitter import TwitterConsumer
    return [TwitterConsumer]

consumers = MultiConsumer(load_consumer_plugins())
consumers.connect()
consumers.start()

