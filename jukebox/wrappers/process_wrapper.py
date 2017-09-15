import subprocess
from threading import Thread, Event
from collections import deque


class NonBlockingStreamReader(object):
    def __init__(self, stream):
        self._stream = stream
        self._queue = deque()
        self._stop = Event()

        def _populate(stream, queue, stop_event):
            while not stop_event.is_set():
                line = stream.readline()
                print line
                if line is not None:
                    queue.append(line)
                elif line is None:
                    return

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
    def __init__(self, stream_reader=None, process_creator=None):
        self._process = None
        self._stream_reader = stream_reader or NonBlockingStreamReader
        self._stdout = None
        self._create_process = process_creator or self._process_creator

    @staticmethod
    def _process_creator(args):
        return subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def launch(self, args):
        self._process = self._create_process(args)
        self._stdout = self._stream_reader(self._process.stdout)

    def poll(self):
        if self._process is not None:
            next_line = self._stdout.readline()
            polled = self._process.poll()
            if next_line == '' and polled is not None:
                self._stdout.terminate()
                return polled

        return None

    def wait(self):
        if self._process and self._process.poll() is None:
            self._process.wait()

    def write(self, command):
        if self._process and self._process.poll() is None:
            self._process.stdin.write(command)

    def clean_up(self):
        if self._stdout:
            self._stdout.terminate()
            self._stdout = None
        self._process = None
