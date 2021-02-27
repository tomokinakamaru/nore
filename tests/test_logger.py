from collections import namedtuple
from logcapture import logcapture
from nore.logger import clogger
from nore.logger import vlogger
from nore.stack import stack


def test_reading_cache():
    msg = 'INFO Reading cache for foo with args=() and kwargs={}'
    with logcapture:
        clogger.reading_cache('foo', (), {})
        assert logcapture.read() == msg


def test_clogger_found_no_cache():
    msg = 'DEBUG Found no cache for foo with args=() and kwargs={}'
    with logcapture:
        clogger.found_no_cache('foo', (), {})
        assert logcapture.read() == msg


def test_found_broken_cache():
    msg = 'DEBUG Found broken cache for foo with args=() and kwargs={}'
    with logcapture:
        clogger.found_broken_cache('foo', (), {})
        assert logcapture.read() == msg


def test_failed_to_read_cache():
    msg = 'WARNING Failed to read cache for foo with args=() and kwargs={}'
    with logcapture:
        clogger.failed_to_read_cache('foo', (), {})
        assert logcapture.read() == msg


def test_running_func():
    msg = 'INFO Running foo with args=() and kwargs={}'
    with logcapture:
        clogger.running_func('foo', (), {})
        assert logcapture.read() == msg


def test_caller_log():
    nt = namedtuple('Bar', 'name')
    obj = nt('bar')
    stack.push(obj)

    msg = 'INFO Running foo with args=() and kwargs={} (from bar)'
    with logcapture:
        clogger.running_func('foo', (), {})
        stack.pop()
        assert logcapture.read() == msg


def test_detected_deletion():
    msg = 'DEBUG Detected deletion of foo'
    with logcapture:
        vlogger.detected_deletion('foo', None)
        assert logcapture.read() == msg


def test_detected_change():
    msg = 'DEBUG Detected change of foo'
    with logcapture:
        vlogger.detected_change('foo', None)
        assert logcapture.read() == msg


def test_vlogger_found_no_cache():
    msg = 'DEBUG Found no cache for foo'
    with logcapture:
        vlogger.found_no_cache('foo', None)
        assert logcapture.read() == msg


def test_found_invalid_cache():
    msg = 'DEBUG Found invalid cache for foo'
    with logcapture:
        vlogger.found_invalid_cache('foo', None)
        assert logcapture.read() == msg


def test_found_broken_deps():
    msg = 'DEBUG Found broken deps file for foo'
    with logcapture:
        vlogger.found_broken_deps('foo', None)
        assert logcapture.read() == msg


def test_found_invalid_cache_propagated():
    msg = 'DEBUG Found invalid cache for foo; propagation from bar'
    with logcapture:
        vlogger.found_invalid_cache_propagated('foo', 'bar', None)
        assert logcapture.read() == msg


def test_parent_log():
    nt = namedtuple('Bar', 'name')
    obj = nt('bar')

    msg = 'DEBUG Detected deletion of foo (dependency of bar)'
    with logcapture:
        vlogger.detected_deletion('foo', obj)
        assert logcapture.read() == msg
