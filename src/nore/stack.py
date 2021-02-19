from threading import get_ident
from .threads import threads


class Stack(object):
    def __init__(self):
        self._stacks = {}

    def empty(self):
        tid = get_ident()
        while True:
            if tid in self._stacks and self._stacks[tid]:
                return False
            if not threads.has_parent(tid):
                break
            tid = threads.get_parent(tid)
        return True

    def peak(self):
        tid = get_ident()
        while True:
            if tid in self._stacks and self._stacks[tid]:
                return self._stacks[tid][-1]
            tid = threads.get_parent(tid)

    def push(self, item):
        self._stacks.setdefault(get_ident(), []).append(item)

    def pop(self):
        tid = get_ident()
        self._stacks[tid].pop()
        if not self._stacks[tid]:
            del self._stacks[tid]
            threads.gc()


stack = Stack()
