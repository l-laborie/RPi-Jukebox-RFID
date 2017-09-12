import logging
import os

from sys import path
path.append(os.getcwd())

from jukebox.handlers import handler_factory
from jukebox.reader import Reader
from jukebox.setting import DAEMON_MAIN_LOOP_TIMEOUT, CMD_SHUTDOWN, LOGGING_FOLDER, LOGGING_LEVEL


class LaunchReader(object):
    def __init__(self):
        print 'initialing ...'
        self.reader = Reader()
        self.handler = handler_factory()
        self.continue_ = True

        if not os.path.exists(LOGGING_FOLDER):
            os.makedirs(LOGGING_FOLDER)
        logging.basicConfig(
            filename=os.path.join(LOGGING_FOLDER, 'jukebox.log'),
            level=LOGGING_LEVEL)
        print 'initiated.'

    def run(self):
        while self.continue_:
            print 'enter loop'
            card_id = self.reader.read_card(
                timeout=DAEMON_MAIN_LOOP_TIMEOUT)

            if not card_id:
                print '--> timeout'
                continue

            if card_id == CMD_SHUTDOWN:
                break

            print 'handle %r' % card_id
            self.handler.command(card_id)
        self.handler.command(CMD_SHUTDOWN)


if __name__ == '__name__':
    print 'launch manually'
    LaunchReader().run()
