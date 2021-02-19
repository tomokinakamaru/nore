import threading
from .threads import threads


class Thread(threading.Thread):
    def start(self):
        threads.lock()
        try:
            super().start()
        except Exception as e:
            raise e
        else:
            threads.set_parent(self.ident)
        finally:
            threads.unlock()
