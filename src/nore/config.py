from . import default


class Config(object):
    def __init__(self):
        self._active = True
        self._cache_path = default.cache_path
        self._locate_cache = default.locate_cache_head

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active: bool):
        self._active = active

    @property
    def cache_path(self):
        return self._cache_path

    @cache_path.setter
    def cache_path(self, cache_path: str):
        self._cache_path = cache_path

    @property
    def locate_cache(self):
        return self._locate_cache

    def cache_locator(self, f: default.locate_cache_head):
        self._locate_cache = f
        return f


config = Config()
