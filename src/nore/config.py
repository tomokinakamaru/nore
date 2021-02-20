from os.path import join


class Config(object):
    def __init__(self):
        self._locate_cache = default_locate_cache
        self._cache_path = default_cache_path
        self._active = True

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    @property
    def locate_cache(self):
        return self._locate_cache

    def cache_locator(self, f):
        self._locate_cache = f
        return f

    @property
    def cache_path(self):
        return self._cache_path

    @cache_path.setter
    def cache_path(self, cache_path):
        self._cache_path = cache_path


def default_locate_cache(name, code_hash):
    name = name.split('.')
    code = code_hash[0], code_hash[1], code_hash[2:]
    return join(*name, *code)


default_cache_path = '.cache'
