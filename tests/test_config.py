from os.path import join
from nore.config import config
from nore import default


def test_active():
    config.active = False
    assert not config.active

    config.active = True
    assert config.active


def test_cache_path():
    config.cache_path = 'foo'
    assert config.cache_path == 'foo'

    config.cache_path = default.cache_path


def test_locate_cache():
    assert config.locate_cache('foo', 'bar') == join('foo', 'b', 'a', 'r')


def test_custom_cache_locator():
    config.cache_locator(lambda *args: 1)
    assert config.locate_cache('foo', 'bar') == 1

    config.cache_locator(default.locate_cache_head)
