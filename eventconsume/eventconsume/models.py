class Model(object):
    """
    The standard model that we use for any event that we receive.
    """

class Event(Model):
    """
    Store data about events.
    """
    def __init__(self, text, location, creator, site):
        if not isinstance(location, tuple):
            raise ValueError('`location` property must be a (lat,long) tuple.')

        self.text = text         # the text content of the event
        self.location = location # the location where this event occurred
        self.creator = creator   # a string describing the event's creator
        self.site = site         # the site where the event originated

class ConsumerError(Model):
    def __init__(self, message, context=None):
        self.message = message
        self.context = context
