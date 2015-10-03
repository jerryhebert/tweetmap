import collections

class Model(object):
    """
    The standard model that we use for any event that we receive.
    """

class Event(Model):
    """
    Store data about events.
    """
    def __init__(self, message, location, creator, site, timestamp):
        if not isinstance(location, collections.Sequence) or len(location) != 2:
            raise ValueError('`location` property must be a sequence of the form (lon,lat)')

        self.message = message       # the message for this event
        self.location = location     # the location where this event occurred
        self.creator = creator       # a string describing the event's creator
        self.site = site             # the site where the event originated
        self.timestamp = timestamp   # timestamp (ms) of when this event was created

class ConsumerError(Model):
    def __init__(self, message, context=None):
        self.message = message
        self.context = context
