from functools import cached_property
from hashlib import md5
from . import default
from .cache import Cache
from .config import config
from .error import BrokenCache
from .error import NoCache
from .logger import clogger
from .stack import stack


class Function(object):
    def __init__(self, func):
        self._func = func
        self._locate_cache = default.locate_cache_tail
        self._check_cache = default.check_cache
        self._read_cache = default.read_cache
        self._write_cache = default.write_cache

    def cache_locator(self, f):
        self._locate_cache = f
        return f

    def cache_checker(self, f):
        self._check_cache = f
        return f

    def cache_reader(self, f):
        self._read_cache = f
        return f

    def cache_writer(self, f):
        self._write_cache = f
        return f

    @cached_property
    def name(self):
        return '.'.join(
            (self._func.__module__, self._func.__qualname__)
        ).replace('<locals>', '$locals')

    @cached_property
    def code(self):
        return self._func.__code__.co_code

    @cached_property
    def code_hash(self):
        return md5(self.code).hexdigest()

    @property
    def locate_cache(self):
        return self._locate_cache

    @property
    def check_cache(self):
        return self._check_cache

    @property
    def read_cache(self):
        return self._read_cache

    @property
    def write_cache(self):
        return self._write_cache

    def __call__(self, *args, **kwargs):
        if not config.active:
            return self._func(*args, **kwargs)

        cache = Cache.from_inv(self, args, kwargs)

        if cache.validate():
            try:
                clogger.reading_cache(self.name, args, kwargs)
                return cache.read()
            except NoCache:
                clogger.found_no_cache(self.name, args, kwargs)
            except BrokenCache:
                clogger.found_broken_cache(self.name, args, kwargs)
            except Exception:
                clogger.failed_to_read_cache(self.name, args, kwargs)

        clogger.running_func(self.name, args, kwargs)

        if not stack.empty():
            stack.peak().dep(cache)
        stack.push(cache)

        try:
            data = self._func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            stack.pop()

        try:
            data = cache.write(data, args, kwargs)
        except Exception as e:
            cache.delete()
            raise e

        return data
