from hashlib import md5
from inspect import isgenerator
from lzma import open
from os.path import isfile
from os.path import join
from pickle import dump
from pickle import dumps
from pickle import load


def locate_cache_head(name, code_hash):
    name = name.split('.')
    code = code_hash[0], code_hash[1], code_hash[2:]
    return join(*name, *code)


def locate_cache_tail(*args, **kwargs):
    kwargs = {k: v for k, v in sorted(kwargs.items())}
    h = md5(dumps((args, kwargs))).hexdigest()
    return join(h[0], h[1], h[2:])


def check_cache(path):
    return isfile(join(path, obj_file_name))


def read_cache(path__, *args, **kwargs):
    obj_path = join(path__, obj_file_name)
    if isfile(join(path__, gen_file_name)):
        return load_many(obj_path)
    return load_one(obj_path)


def write_cache(path__, data__, *args, **kwargs):
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


cache_path = '.cache'

obj_file_name = 'obj.gzip'

gen_file_name = 'gen'
