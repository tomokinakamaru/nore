from threading import enumerate
from threading import get_ident
from threading import Lock


class Threads(object):
    def __init__(self):
        self._starters = {}
        self._lock = Lock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def get_starter(self, tid):
        with self._lock:
            return self._starters.get(tid)

    def set_starter(self, tid):
        self._starters[tid] = get_ident()

    def gc(self):
        tids = [t.ident for t in enumerate()]
        with self._lock:
            for t in list(self._starters):
                if t not in tids:
                    del self._starters[t]


threads = Threads()
