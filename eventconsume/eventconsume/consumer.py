import abc
import os
import sys
import yaml
import logging

from eventconsume.exceptions import ConsumerConfigError

class Consumer(object):
    """
    Abstract consumer for any generic event type. Specific
    types of consumers should subclass this and implement
    these methods.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        """
        Load the config from the file relative to where ever our plugin is.
        It might just be better to specify these explicitly since this is
        a bit ugly but now a new plugin never has to worry about pointing
        its module to its config.
        """
        m = sys.modules[self.__class__.__module__]
        try:
            base, fname = os.path.split(os.path.realpath(m.__file__))
            fname = os.path.splitext(fname)[0] + '.yml'
            final = os.path.join(base, fname)
            with open(final) as config_file:
                config = yaml.load(config_file.read())
        except (IOError, ValueError) as exc:
            logging.error(('Failed to find config file for module: ' + self.__class__.__module__ +
                'Configure the following file before using this plugin:\n' +
                '\t' + final))
            raise ConsumerConfigError

        return config

    @abc.abstractmethod
    def connect(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def start(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self, event):
        raise NotImplementedError

