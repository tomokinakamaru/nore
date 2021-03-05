from threading import current_thread
from nore import Thread
from pytest import raises


def test_normal():
    t = Thread(target=lambda: ...)
    t.start()
    t.join()
    assert t._starter == current_thread()


def test_exception():
    t = Thread(target=lambda: ...)
    t.start()
    t.join()
    with raises(RuntimeError):
        t.start()
