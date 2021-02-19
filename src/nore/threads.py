from threading import enumerate
from threading import get_ident
from threading import Lock


class Threads(object):
    def __init__(self):
        self._parents = {}
        self._lock = Lock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def get_parent(self, tid):
        with self._lock:
            return self._parents.get(tid)

    def set_parent(self, tid):
        self._parents[tid] = get_ident()

    def gc(self):
        tids = [t.ident for t in enumerate()]
        with self._lock:
            for t in list(self._parents):
                if t not in tids:
                    del self._parents[t]


threads = Threads()
