from threading import current_thread
from threading import get_ident


class Stack(object):
    def __init__(self):
        self._stacks = {}

    def empty(self):
        thread = current_thread()
        while thread:
            tid = thread.ident
            if tid in self._stacks and self._stacks[tid]:
                return False
            thread = getattr(thread, '_starter', None)
        return True

    def peak(self):
        thread = current_thread()
        while thread:
            tid = thread.ident
            if tid in self._stacks and self._stacks[tid]:
                return self._stacks[tid][-1]
            thread = getattr(thread, '_starter', None)

    def push(self, item):
        self._stacks.setdefault(get_ident(), []).append(item)

    def pop(self):
        tid = get_ident()
        self._stacks[tid].pop()
        if not self._stacks[tid]:
            del self._stacks[tid]


stack = Stack()
