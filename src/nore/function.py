from copy import deepcopy
from functools import cached_property
from hashlib import md5
from inspect import isgenerator
from lzma import open
from os.path import isfile
from os.path import join
from pickle import dump
from pickle import dumps
from pickle import load
from . import logger
from .cache import Cache
from .error import BrokenCache
from .nocache import NoCache
from .stack import stack


class Function(object):
    def __init__(self, func, config):
        self._func = func
        self._locate_cache = default_locate_cache
        self._check_cache = default_check_cache
        self._read_cache = default_read_cache
        self._write_cache = default_write_cache
        self._config = config

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
        return '.'.join((self._func.__module__, self._func.__qualname__))

    @cached_property
    def code(self):
        return self._func.__code__.co_code

    @cached_property
    def code_hash(self):
        return md5(self.code).hexdigest()

    @property
    def read_cache(self):
        return self._read_cache

    @property
    def write_cache(self):
        return self._write_cache

    @property
    def check_cache(self):
        return self._check_cache

    @property
    def locate_cache(self):
        return self._locate_cache

    def __call__(self, *args, **kwargs):
        if not self._config.active:
            return self._func(*args, **kwargs)

        cache = Cache.from_inv(self, args, kwargs, self._config)
        log_suffix = f'with args={args} and kwargs={kwargs}'

        if cache.validate():
            try:
                info(f'Reading cache for {self.name} {log_suffix}')
                return cache.read()
            except NoCache:
                debug(f'Found no cache for {self.name} {log_suffix}')
            except BrokenCache:
                debug(f'Found broken cache for {self.name} {log_suffix}')
            except Exception:
                warn(f'Failed to read cache for {self.name} {log_suffix}')

        info(f'Running {self.name} {log_suffix}')
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


def default_locate_cache(*args, **kwargs):
    kwargs = {k: v for k, v in sorted(kwargs.items())}
    h = md5(dumps(deepcopy((args, kwargs)))).hexdigest()
    return join(h[0], h[1], h[2:])


def default_check_cache(path):
    return isfile(join(path, obj_file_name))


def default_read_cache(path__, *args, **kwargs):
    obj_path = join(path__, obj_file_name)
    if isfile(join(path__, gen_file_name)):
        return load_many(obj_path)
    return load_one(obj_path)


def default_write_cache(path__, data__, *args, **kwargs):
    gen_path = join(path__, gen_file_name)
    obj_path = join(path__, obj_file_name)
    if isgenerator(data__):
        open(gen_path, 'wb').close()
        dump_many(obj_path, data__)
        return load_many(obj_path)
    dump_one(obj_path, data__)
    return data__


def load_one(path):
    with open(path, 'rb') as f:
        return load(f)


def load_many(path):
    with open(path, 'rb') as f:
        while True:
            try:
                yield load(f)
            except EOFError:
                break


def dump_one(path, data):
    with open(path, 'wb') as f:
        dump(data, f)


def dump_many(path, data):
    with open(path, 'wb') as f:
        for e in data:
            dump(e, f)


def debug(msg):
    log(logger.debug, msg)


def info(msg):
    log(logger.info, msg)


def warn(msg):
    log(logger.warn, msg)


def log(func, msg):
    if not stack.empty():
        msg += f' (from {stack.peak().name})'
    func(msg)


obj_file_name = 'obj.gzip'

gen_file_name = 'gen'
