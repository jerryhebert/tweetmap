import abc

class Consumer(object):
    """
    Abstract consumer for any generic event type.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def connect(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def start(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self, event):
        raise NotImplementedError

