import subprocess
from threading import Thread, Event
from collections import deque


class UnexpectedEndOfStream(Exception):
    pass


class NonBlockingStreamReader(object):
    def __init__(self, stream):
        self._stream = stream
        self._queue = deque()
        self._stop = Event()

        def _populate(stream, queue, stop_event):
            while not stop_event.is_set():
                line = stream.readline()
                if line is not None:
                    queue.append(line)
                elif line is None:
                    raise UnexpectedEndOfStream

        self._thread = Thread(
            target=_populate,
            args=(self._stream, self._queue, self._stop))
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

    def launch(self, args):
        print args
        self._process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._nbsr = NonBlockingStreamReader(
            self._process.stdout)

    def poll(self):
        if self._process is not None:
            next_line = self._nbsr.readline()
            polled = self._process.poll()
            if next_line == '' and polled is not None:
                self._nbsr.terminate()
                return polled

        return None

    def wait(self):
        if self._process and self._process.poll() is None:
            self._process.wait()

    def write(self, command):
        print 'enter write %s' % command
        print self._process and self._process.poll() is None
        if self._process and self._process.poll() is None:
            self._process.stdin.write(command)
            print 'wrote'

    def clean_up(self):
        print 'clean up'
        if self._nbsr:
            self._nbsr.terminate()
            self._nbsr = None
        self._process = None

