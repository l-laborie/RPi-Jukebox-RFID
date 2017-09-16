import logging
import os

from sys import path
path.append(os.getcwd())

# pylint: disable=wrong-import-position
from jukebox.handlers import handler_factory  # noqa
from jukebox.reader import Reader  # noqa
from jukebox.setting import (  # noqa
    DAEMON_MAIN_LOOP_TIMEOUT,
    CMD_SHUTDOWN,
    LOGGING_FOLDER,
    LOGGING_LEVEL,
)


class LaunchReader(object):
    def __init__(self):
        self.reader = Reader()
        self.handler = handler_factory()
        self.continue_ = True

        if not os.path.exists(LOGGING_FOLDER):
            os.makedirs(LOGGING_FOLDER)
        logging.basicConfig(
            filename=os.path.join(LOGGING_FOLDER, 'jukebox.log'),
            level=LOGGING_LEVEL)

    def run(self):
        while self.continue_:
            card_id = self.reader.read_card(
                timeout=DAEMON_MAIN_LOOP_TIMEOUT)

            if not card_id:
                continue

            if card_id == CMD_SHUTDOWN:
                break

            self.handler.command(card_id)
        self.handler.command(CMD_SHUTDOWN)


LaunchReader().run()

