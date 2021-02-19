from . import gc
from . import nocache
from .config import config
from .function import Function
from .functions import functions


class Api(object):
    def __call__(self, f):
        func = Function(f)
        functions.put(func)
        return func

    def activate(self):
        config.active = True

    def deactivate(self):
        config.active = False

    def nocache(self, f):
        func = self(f)
        func.cache_locator(nocache.locate_cache)
        func.cache_checker(nocache.check_cache)
        func.cache_reader(nocache.read_cache)
        func.cache_writer(nocache.write_cache)
        return func

    def gc(self):
        gc.run()

    def cache_locator(self, f):
        return config.cache_locator(f)

    @property
    def cache_path(self):
        return config.cache_path

    @cache_path.setter
    def cache_path(self, cache_path):
        config.cache_path = cache_path

    @property
    def lifetime(self):
        return config.lifetime

    @lifetime.setter
    def lifetime(self, lifetime):
        config.lifetime = lifetime


api = Api()
