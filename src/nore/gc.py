from datetime import datetime
from logging import getLogger
from os import walk
from os import listdir
from os.path import isdir
from os.path import join
from shutil import rmtree
from time import time
from .cache import cache_dir_ext
from .cache import time_file_name


def gc(path, lifetime: int):
    remove_unused_caches(path, lifetime)
    remove_empty_dirs(path)


def remove_unused_caches(path, lifetime):
    for root, dirs, _ in walk(path):
        for dir in dirs:
            if dir.endswith(cache_dir_ext):
                remove_unused_cache(join(root, dir), lifetime)


def remove_unused_cache(path, lifetime):
    t = read_time(join(path, time_file_name))
    dt = datetime.fromtimestamp(int(t))
    debug(f'Cache at {shorten(path)} is touched at {dt}')
    if t + lifetime < time():
        debug(f'Removing recently untouched cache at {shorten(path)}')
        rmtree(path)


def read_time(path):
    try:
        with open(path) as f:
            return float(f.read())
    except Exception as e:
        debug(f'Time file of {shorten(path)} is broken: {e}')
        return 0


def remove_empty_dirs(path):
    files = listdir(path)
    if files:
        for f in files:
            p = join(path, f)
            if isdir(p):
                remove_empty_dirs(p)

    files = listdir(path)
    if not files:
        debug(f'Removing empty directory at {shorten(path)}')
        rmtree(path)


def shorten(path):
    if 59 < len(path):
        return path[:27] + ' ... ' + path[-28:]
    return path


def debug(msg):
    getLogger('nore').debug(msg)
