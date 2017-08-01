import os
import signal
from sys import path

import daemon
import lockfile
path.append(os.getcwd())

# pylint: disable=wrong-import-position
from jukebox.reader import Reader  # noqa
from jukebox.handlers import handler_factory  # noqa


WORKING_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))


class DaemonReader(object):
    def __init__(self):
        self.context = daemon.DaemonContext(
            working_directory=WORKING_DIRECTORY,
            umask=0o002,
            pidfile=lockfile.FileLock('/var/run/RPI-jukebox-RFID.pid'),
            stdout=open(os.path.join(
                WORKING_DIRECTORY, 'logs', 'STDOUT'), 'w+'),
            stderr=open(os.path.join(
                WORKING_DIRECTORY, 'logs', 'STDERR'), 'w+'),
        )
        self.context.signal_map = {
            signal.SIGTERM: 'terminate',
            signal.SIGHUP: 'terminate',
        }
        # init
        self.reader = Reader()
        self.handler = handler_factory()

    def run(self):
        # main
        with self.context:
            while True:
                card_id = self.reader.read_card()
                self.handler.command(card_id)


if __name__ == '__main__':
    DaemonReader().run()
