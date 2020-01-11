from abc import abstractmethod


class Engine:
    def __init__(self):
        self._name = 'unknown_engine'

    @property
    def name(self):
        return self._name

    @abstractmethod
    def start(self):
        self._raise_not_implemented_error('start')

    @abstractmethod
    def stop(self):
        self._raise_not_implemented_error('start')

    @abstractmethod
    def search(self, *args, **kwargs):
        self._raise_not_implemented_error('search')

    def _raise_not_implemented_error(self, method_name):
        raise NotImplementedError('{} class missing required implementation of method: {}'.format(self.__class__.__name__, method_name))
