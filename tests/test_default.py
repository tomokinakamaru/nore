from nore import default
from os import remove
from os.path import join


def test_locate_cache_head():
    assert default.locate_cache_head('foo', 'bar') == join(
        'foo', 'b', 'a', 'r'
    )


def test_locate_cache_tail():
    assert default.locate_cache_tail((), {}) == join(
        '0', 'f', '28a9a72b38fbccc9810bf4c433558a'
    )


def test_check_cache():
    assert default.check_cache(join('tests', 'resource', 'data1'))
    assert not default.check_cache('.')


def test_read_cache():
    assert default.read_cache(join('tests', 'resource', 'data1')) == 0


def test_read_cache_generator():
    g = default.read_cache(join('tests', 'resource', 'data2'))
    assert tuple(g) == (0, 1)


def test_write_cache():
    path = join('tests', 'workspace')
    obj = default.write_cache(path, 0)
    assert obj == 0
    remove(join(path, 'obj.gzip'))


def test_write_cache_generator():
    path = join('tests', 'workspace')
    gen = default.write_cache(path, (i for i in range(2)))
    assert tuple(gen) == (0, 1)
    remove(join(path, 'gen'))
    remove(join(path, 'obj.gzip'))
