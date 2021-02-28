import inspect
import nore
from logcapture import logcapture
from nore import default
from nore.functions import functions
from os import remove
from os.path import join
from pytest import raises
from shutil import rmtree


def test_cache1():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x
        assert f(1) == 1
        assert f(1) == 1
        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={}',
            'INFO Reading cache for f with args=(1,) and kwargs={}'
        )


def test_cache2():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x

        @nore.cache
        def g(x):
            return f(x)

        assert g(1) == 1
        assert g(1) == 1
        assert read_log() == (
            'DEBUG Found no cache for g',
            'INFO Running g with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={} (from g)',
            'INFO Reading cache for g with args=(1,) and kwargs={}',
        )


def test_different_arg():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x
        assert f(1) == 1
        assert f(2) == 2
        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f',
            'INFO Running f with args=(2,) and kwargs={}',
        )


def test_change1():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x
        assert f(1) == 1

        clear_funcs()

        @nore.cache
        def f(x):
            return x + 1
        assert f(1) == 2

        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={}',
        )


def test_change2():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x

        @nore.cache
        def g(x):
            return f(x)

        assert g(1) == 1

        clear_funcs()

        @nore.cache
        def f(x):  # noqa
            return x

        @nore.cache
        def g(x):
            return f(x) + 1

        assert g(1) == 2

        assert read_log() == (
            'DEBUG Found no cache for g',
            'INFO Running g with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={} (from g)',
            'DEBUG Found no cache for g',
            'INFO Running g with args=(1,) and kwargs={}',
            'INFO Reading cache for f with args=(1,) and kwargs={} (from g)'
        )


def test_nocache():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.nocache
        def f(x):
            return x
        assert f(1) == 1
        assert f(1) == 1
        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={}',
            'INFO Reading cache for f with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f with args=(1,) and kwargs={}',
            'INFO Running f with args=(1,) and kwargs={}',
        )


def test_deactivate():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x

        nore.config.active = False
        assert f(1) == 1
        nore.config.active = True
        assert read_log() == ()


def test_dependency_update():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x

        @nore.cache
        def g(x):
            return f(x)

        assert g(1) == 1

        clear_funcs()

        @nore.cache
        def f(x):  # noqa
            return x + 1

        @nore.cache
        def g(x):
            return f(x)

        assert g(1) == 2

        assert read_log() == (
            'DEBUG Found no cache for g',
            'INFO Running g with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={} (from g)',
            'DEBUG Detected change of f (dependency of g)',
            'DEBUG Found invalid cache for g; propagation from f',
            'INFO Running g with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={} (from g)'
        )


def test_dependency_delete():
    clear_cache()
    clear_funcs()
    with logcapture:
        @nore.cache
        def f(x):
            return x

        func = f

        @nore.cache
        def g(x):
            return func(x)

        assert g(1) == 1

        clear_funcs()

        @nore.cache
        def h(x):
            return x + 1

        func = h

        @nore.cache
        def g(x):
            return func(x)

        assert g(1) == 2

        assert read_log() == (
            'DEBUG Found no cache for g',
            'INFO Running g with args=(1,) and kwargs={}',
            'DEBUG Found no cache for f',
            'INFO Running f with args=(1,) and kwargs={} (from g)',
            'DEBUG Detected deletion of f (dependency of g)',
            'DEBUG Found invalid cache for g; propagation from f',
            'INFO Running g with args=(1,) and kwargs={}',
            'DEBUG Found no cache for h',
            'INFO Running h with args=(1,) and kwargs={} (from g)'
        )


def test_exception():
    with logcapture:
        @nore.cache
        def f():
            raise RuntimeError()

        with raises(RuntimeError):
            f()


def test_broken_cache_writer1():
    with logcapture:
        @nore.cache
        def f():
            return

        @f.cache_writer
        def _():
            pass

        with raises(TypeError):
            f()


def test_broken_cache_writer2():
    with logcapture:
        @nore.cache
        def f():
            return

        @f.cache_writer
        def _(path, data, *args, **kwargs):
            pass

        f()
        f()

        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=() and kwargs={}',
            'DEBUG Found invalid cache for f',
            'INFO Running f with args=() and kwargs={}'
        )


def test_broken_cache_writer3():
    with logcapture:
        @nore.cache
        def f():
            return

        @f.cache_writer
        def _(path, data, *args, **kwargs):
            open(join(path, 'obj.gzip'), 'w').close()
            remove(join(path, '..', 'deps'))

        f()
        f()

        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=() and kwargs={}',
            'DEBUG Found broken deps file for f',
            'INFO Running f with args=() and kwargs={}'
        )


def test_broken_cache_writer4():
    with logcapture:
        @nore.cache
        def f():
            return

        @f.cache_writer
        def _(path, data, *args, **kwargs):
            open(join(path, 'obj.gzip'), 'w').close()

        f()
        f()

        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=() and kwargs={}',
            'INFO Reading cache for f with args=() and kwargs={}',
            'WARNING Failed to read cache for f with args=() and kwargs={}',
            'INFO Running f with args=() and kwargs={}'
        )


def test_broken_cache_writer5():
    with logcapture:
        @nore.cache
        def f():
            return

        global data_path
        data_path = None

        @f.cache_writer
        def _(path, data, *args, **kwargs):
            global data_path
            data_path = path
            default.write_cache(path, data, *args, **kwargs)

        f()

        open(join(data_path, '..', 'tran'), 'w').close()

        f()

        assert read_log() == (
            'DEBUG Found no cache for f',
            'INFO Running f with args=() and kwargs={}',
            'INFO Reading cache for f with args=() and kwargs={}',
            'DEBUG Found broken cache for f with args=() and kwargs={}',
            'INFO Running f with args=() and kwargs={}'
        )


def clear_cache():
    rmtree(nore.config.cache_path, ignore_errors=True)


def clear_funcs():
    functions._funcs.clear()


def read_log():
    log = logcapture.read()
    caller = inspect.stack()[1].function
    return tuple(log.replace(f'test_nore.{caller}.$locals.', '').splitlines())
