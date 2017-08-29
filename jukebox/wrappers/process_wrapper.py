import subprocess


class ProcessWrapper(object):
    def __init__(self):
        self._process = None

    def launch(self, args):
        self._process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def poll(self):
        if self._process is not None:
            next_line = self._process.stdout.readline()
            polled = self._process.poll()
            if next_line == '' and polled is not None:
                return polled

        return None

    def wait(self):
        if self._process is not None:
            self._process.wait()

    def write(self, command):
        if self._process is not None:
            self._process.stdin.write(command)

    def clean_up(self):
        self._process = None
