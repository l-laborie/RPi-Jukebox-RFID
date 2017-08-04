import logging
import os
import signal
from sys import path

import daemon
import lockfile
path.append(os.getcwd())

# pylint: disable=wrong-import-position
from jukebox.reader import Reader  # noqa
from jukebox.handlers import handler_factory  # noqa
from jukebox.setting import (  # noqa
    LOGGING_FOLDER,
    LOGGING_LEVEL,
    WORKING_DIRECTORY,
    DAEMON_MAIN_LOOP_TIMEOUT,
    CMD_SHUTDOWN,
)


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
            signal.SIGTERM: self.terminate,
            signal.SIGHUP: self.terminate,
        }
        # init
        self.reader = Reader()
        self.handler = handler_factory()
        self.continue_ = True

        if not os.path.exists(LOGGING_FOLDER):
            os.makedirs(LOGGING_FOLDER)
        logging.basicConfig(
            filename=path.join(LOGGING_FOLDER, 'jukebox.log'),
            level=LOGGING_LEVEL)

    def terminate(self):
        self.continue_ = False

    def run(self):
        # main
        with self.context:
            while self.continue_:
                card_id = self.reader.read_card(
                    timeout=DAEMON_MAIN_LOOP_TIMEOUT)

                if not card_id:
                    continue

                if card_id == CMD_SHUTDOWN:
                    break

                self.handler.command(card_id)
            self.handler.command(CMD_SHUTDOWN)


if __name__ == '__main__':
    DaemonReader().run()
