from threading import Thread as Thread_
from .threads import threads


class Thread(Thread_):
    def start(self):
        threads.lock()
        try:
            super().start()
        except Exception as e:
            raise e
        else:
            threads.set_starter(self.ident)
        finally:
            threads.unlock()
