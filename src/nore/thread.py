from threading import current_thread
from threading import Thread as Thread_


class Thread(Thread_):
    def start(self):
        self._starter = current_thread()
        super().start()
