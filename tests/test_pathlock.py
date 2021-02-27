from nore.pathlock import pathlock


def test_lock():
    with pathlock.lock('foo'):
        assert 'foo' in pathlock._locks
        assert len(pathlock._locks) == 1

    with pathlock.lock('bar'):
        assert 'bar' in pathlock._locks
        assert len(pathlock._locks) == 1
