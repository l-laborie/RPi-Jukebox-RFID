import logging
import subprocess


LOGGER = logging.getLogger('ProcessWrapper')


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
        LOGGER.debug('Enter poll')
        if self._process is not None:
            next_line = self._process.stdout.readline()
            polled = self._process.poll()
            LOGGER.debug('line seen %s, poll result %r' % (next_line, polled))
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
