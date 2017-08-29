from collections import deque
from threading import Lock


class LockedQueue(object):
    def __init__(self, maxsize=10):
        self._lock = Lock()
        self._queue = deque(maxlen=maxsize)

    def push(self, *items):
        with self._lock:
            for item in items:
                self._queue.append(item)

    def pop(self):
        if self.empty():
            return None

        with self._lock:
            return self._queue.popleft()

    def empty(self):
        with self._lock:
            return not self._queue
