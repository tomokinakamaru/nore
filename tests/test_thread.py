from threading import get_ident
from nore import Thread
from nore.threads import threads
from pytest import raises


def test_normal():
    t = Thread(target=lambda: ...)
    t.start()
    t.join()
    assert threads.get_starter(t.ident) == get_ident()


def test_exception():
    t = Thread(target=lambda: ...)
    t.start()
    t.join()
    with raises(RuntimeError):
        t.start()


def test_gc():
    t = Thread(target=lambda: ...)
    t.start()
    t.join()
    threads.gc()
    assert len(threads._starters) == 0
