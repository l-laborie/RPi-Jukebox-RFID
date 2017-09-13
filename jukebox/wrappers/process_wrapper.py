import subprocess
from threading import Thread, Event
from collections import deque


class UnexpectedEndOfStream(Exception):
    pass


class NonBlockingStreamReader(object):
    def __init__(self, stream, callback=None):
        def _default_callback():
            raise UnexpectedEndOfStream

        self._stream = stream
        self._queue = deque()
        self._stop = Event()
        self._callback = callback or _default_callback

        def _populate(stream, queue, stop_event, callback_):
            while not stop_event.is_set():
                line = stream.readline()
                if line is not None:
                    queue.append(line)
                elif line is None:
                    callback_()

        self._thread = Thread(
            target=_populate,
            args=(self._stream, self._queue, self._stop, self._callback))
        self._thread.daemon = True
        self._thread.start()

    def readline(self):
        if self._queue:
            return self._queue.popleft()

    def terminate(self):
        self._stop.set()


class ProcessWrapper(object):
    def __init__(self):
        self._process = None
        self._nbsr = None

    @staticmethod
    def _create_process(args):
        return subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def launch(self, args):
        self._process = self._create_process(args)
        self._nbsr = NonBlockingStreamReader(
            self._process.stdout,
        )

    def poll(self):
        if self._process:
            next_line = self._nbsr.readline()
            polled = self._process.poll()
            if next_line == '' and polled is not None:
                return polled

        return None

    def wait(self):
        if self._process and self._process.poll() is None:
            self._process.wait()

    def write(self, command):
        if self._process and self._process.poll() is None:
            self._process.stdin.write(command)

    def clean_up(self):
        if self._nbsr:
            self._nbsr.terminate()
            self._nbsr = None
        self._process = None
