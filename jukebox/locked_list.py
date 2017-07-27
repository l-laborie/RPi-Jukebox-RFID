from threading import Lock


class LockedList(object):
    def __init__(self, data=None):
        if data is not None:
            assert isinstance(data, list)
        self._lock = Lock()
        self._data = data or []
        self._index = 0 if len(self._data) > 0 else None

    def set(self, data):
        assert isinstance(data, list)
        with self._lock:
            self._data = data
            self._index = 0 if len(self._data) > 0 else None

    def get(self):
        return self._data[self._index]

    def increase_index(self):
        old_index = self._index
        with self._lock:
            if self._index is not None:
                self._index = min(len(self._data) - 1, self._index + 1)
        return self._index > old_index

    def decrease_index(self):
        old_index = self._index
        with self._lock:
            if self._index is not None:
                self._index = max(0, self._index - 1)
        return self._index < old_index
