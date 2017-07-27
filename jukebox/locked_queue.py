from Queue import Queue
from threading import Lock


class LockedQueue(object):
    def __init__(self, maxsize=10):
        self._lock = Lock()
        self._queue = Queue(maxsize=maxsize)

    def push(self, *items):
        with self._lock:
            for item in items:
                self._queue.put(item)

    def pop(self):
        with self._lock:
            return self._queue.get()

    def empty(self):
        with self._lock:
            return self._queue.empty()
