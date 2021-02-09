from .error import NoCache


def locate_cache(*args, **kwargs):
    return nocache_dir_name


def check_cache(path):
    return True


def read_cache(path__, *args, **kwargs):
    raise NoCache()


def write_cache(path__, data__, *args, **kwargs):
    return data__


nocache_dir_name = '.nocache'
