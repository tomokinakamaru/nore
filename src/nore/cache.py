import lzma
from functools import cached_property
from os import makedirs
from os import remove
from os.path import exists
from os.path import isdir
from os.path import join
from pickle import dump
from pickle import load
from shutil import rmtree
from time import time
from .config import config
from .error import BrokenCache
from .functions import functions
from .logger import vlogger
from .pathlock import pathlock


class Cache(object):
    @classmethod
    def from_inv(cls, func, args, kwargs):
        return cls(func, args, kwargs, None, None, None)

    @classmethod
    def from_dep(cls, name, code_hash, args_path):
        return cls(None, None, None, name, code_hash, args_path)

    def __init__(self, func, args, kwargs, name, code_hash, args_path):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._name = name
        self._code_hash = code_hash
        self._args_path = args_path
        self._deps = set()

    @cached_property
    def name(self):
        return self._name if self._name else self._func.name

    @cached_property
    def code_hash(self):
        return self._code_hash if self._code_hash else self._func.code_hash

    @cached_property
    def args_path(self):
        if self._args_path:
            return self._args_path
        return self._func.locate_cache(*self._args, **self._kwargs)

    @cached_property
    def path(self):
        return join(
            config.cache_path,
            config.locate_cache(self.name, self.code_hash),
            self.args_path + cache_dir_ext
        )

    @cached_property
    def data_path(self):
        return join(self.path, data_dir_name)

    @cached_property
    def deps_path(self):
        return join(self.path, deps_file_name)

    @cached_property
    def time_path(self):
        return join(self.path, time_file_name)

    @cached_property
    def tran_path(self):
        return join(self.path, tran_file_name)

    def dep(self, cache):
        self._deps.add(cache)

    def read(self):
        if exists(self.tran_path):
            self.delete()
            raise BrokenCache()
        with pathlock.lock(self.path):
            self.touch()
            return self._func.read_cache(self.data_path)

    def write(self, data):
        with pathlock.lock(self.path):
            makedirs(self.data_path, exist_ok=True)
            self.begin_tran()
            self.touch()
            self.dump_deps()
            data = self._func.write_cache(self.data_path, data)
            self.end_tran()
            return data

    def delete(self):
        with pathlock.lock(self.path):
            rmtree(self.path, ignore_errors=True)

    def validate(self, parent=None):
        if not functions.has(self.name):
            vlogger.detected_deletion(self.name, parent)
            return False

        if not functions.has(self.name, self.code_hash):
            vlogger.detected_change(self.name, parent)
            return False

        if not isdir(self.data_path):
            vlogger.found_no_cache(self.name, parent)
            return False

        func = functions.get(self.name, self.code_hash)
        if not func.check_cache(self.data_path):
            vlogger.found_invalid_cache(self.name, parent)
            return False

        deps = self.load_deps()
        if not isinstance(deps, set):
            vlogger.found_broken_deps(self.name, parent)
            return False

        for name, code_hash, args_path in deps:
            cache = Cache.from_dep(name, code_hash, args_path)
            if not cache.validate(self):
                vlogger.found_invalid_cache_propagated(self.name, name, parent)
                return False

        self.touch()
        return True

    def begin_tran(self):
        open(self.tran_path, 'wb').close()

    def end_tran(self):
        remove(self.tran_path)

    def touch(self):
        with open(self.time_path, 'w') as f:
            f.write(str(time()))

    def load_deps(self):
        try:
            with lzma.open(self.deps_path, 'rb') as f:
                return load(f)
        except Exception:
            return None

    def dump_deps(self):
        with lzma.open(self.deps_path, 'wb') as f:
            deps = {(c.name, c.code_hash, c.args_path) for c in self._deps}
            dump(deps, f)


cache_dir_ext = '.cache'

data_dir_name = 'data'

deps_file_name = 'deps'

time_file_name = 'time'

tran_file_name = 'tran'
