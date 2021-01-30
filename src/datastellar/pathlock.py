from threading import Lock


class PathLock(object):
    def __init__(self):
        self._lock = Lock()
        self._locks = {}

    def lock(self, path):
        with self._lock:
            self._locks.setdefault(path, Lock())
            for p, lock in list(self._locks.items()):
                if not lock.locked() and p != path:
                    del self._locks[p]
            return self._locks[path]


pathlock = PathLock()
