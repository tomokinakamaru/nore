from . import gc
from . import nocache
from .config import Config
from .function import Function
from .functions import functions
from .logger import logger


class Nore(object):
    def __init__(self):
        self._config = Config()

    def __call__(self, f):
        func = Function(f, self._config)
        functions.put(func)
        return func

    def nocache(self, f):
        func = self(f)
        func.cache_locator(nocache.locate_cache)
        func.cache_checker(nocache.check_cache)
        func.cache_reader(nocache.read_cache)
        func.cache_writer(nocache.write_cache)
        return func

    def gc(self, seconds=0, minutes=0, hours=0, days=0):
        lifetime = seconds
        lifetime += minutes * 60
        lifetime += hours * 60 * 60
        lifetime += days * 60 * 60 * 24
        gc.run(self.config.cache_path, lifetime)

    @property
    def logger(self):
        return logger

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def cache_locator(self, f):
        return self._config.cache_locator(f)

    @property
    def cache_path(self):
        return self._config.cache_path

    @cache_path.setter
    def cache_path(self, cache_path):
        self._config.cache_path = cache_path
