import nore
from logcapture import logcapture
from nore import default
from os.path import join
from shutil import rmtree


def test_gc():
    rmtree(nore.config.cache_path, ignore_errors=True)

    @nore.cache
    def f(x):
        return x

    assert f(1) == 1

    with logcapture:
        nore.gc('.cache', 0)
        assert len(logcapture.read()) == 917


def test_gc_error():
    rmtree(nore.config.cache_path, ignore_errors=True)

    @nore.cache
    def f(x):
        return x

    @f.cache_writer
    def _(path, data):
        default.write_cache(path, data)
        open(join(path, '..', 'time'), 'w').close()
        return data

    assert f(1) == 1

    with logcapture:
        nore.gc('.cache', 0)
        assert len(logcapture.read()) == 1076
