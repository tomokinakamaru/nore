from .error import NoCache
from .function import Function
from .functions import functions


def cache(f):
    func = Function(f)
    functions.put(func)
    return func


def nocache(f):
    func = cache(f)
    func.cache_locator(nocache_locate_cache)
    func.cache_checker(nocache_check_cache)
    func.cache_reader(nocache_read_cache)
    func.cache_writer(nocache_write_cache)
    return func


def nocache_locate_cache(*args, **kwargs):
    return nocache_dir_name


def nocache_check_cache(path):
    return True


def nocache_read_cache(path__, *args, **kwargs):
    raise NoCache()


def nocache_write_cache(path__, data__, *args, **kwargs):
    return data__


nocache_dir_name = '.nocache'
