from datetime import datetime
import deamon
import lockfile
import logging
import logging.handlers
from os import path
import signal

from jukebox.players.OMXPlayer import OMXPlayer
from jukebox.setting import (
    WORKING_DIRECTORY,
    PLAYER_STARTUP_SOUND,
    PLAYER_HALT_SOUND,
    LOGGING_LEVEL,
    LOGGING_FILE,
    CMD_MUTE,
    CMD_NEXT,
    CMD_PREVIOUS,
    CMD_SHUTDOWN,
    CMD_STOP,
    CMD_VOL_MINUS,
    CMD_VOL_PLUS,
)
from jukebox.reader import Reader


LOGGER = logging.getLogger('Daemon')


class Service(object):

    exit_flag = 0

    def __init__(self):
        # Configure the logger
        logging.basicConfig(
            filename=LOGGING_FILE,
            filemode='w',
            level=LOGGING_LEVEL,
            format='[%(asctime)s] %(levelname)s:%(message)s',
            datefmt='%Y/%m/%d %H:%M:%S'
        )

        LOGGER.info('Start the daemon')

        self.player = OMXPlayer()
        if PLAYER_STARTUP_SOUND:
            self.player.play(PLAYER_STARTUP_SOUND)

        self.reader = Reader()

    def __del__(self):
        if PLAYER_STARTUP_SOUND:
            self.player.play(PLAYER_STARTUP_SOUND)

        self.player.quit()
        self._halt()

    def _halt(self):
        # TODO: create a efficient shutdown, the same with timer
        pass

    def main_loop(self):
        while not self.exit_flag:
            # reading the card id
            card_id = self.reader.read_card()

            # start the player script and pass on the cardid
            if card_id == CMD_VOL_PLUS:
                self.player.increase_volume()
            elif card_id == CMD_VOL_MINUS:
                self.player.decrease_volume()
            elif card_id == CMD_STOP:
                self.player.stop()
            elif card_id == CMD_PREVIOUS:
                self.player.previous_media()
            elif card_id == CMD_NEXT:
                self.player.next_media()
            elif card_id == CMD_MUTE:
                # TODO: may be player pause ?
                pass
            elif card_id == CMD_SHUTDOWN:
                self._halt()
            else:
                now = datetime.now()
                latest_id = path.join(WORKING_DIRECTORY, 'shared',
                                         'latestID.txt')
                with open(latest_id, 'w') as latest_id_file:
                    latest_id_file.write('Card ID %s was used at %s.' % (
                        card_id, now.strftime('%Y/%m/%d %H:%M')))

                    shortcut = path.join(WORKING_DIRECTORY, 'shared',
                                            'shortcuts', card_id)
                    if path.isfile(shortcut):
                        with open(shortcut, 'r') as shortcut_file:
                            folder = shortcut_file.read()
                        media_folder = os.path.join(WORKING_DIRECTORY, 'shared',
                                                    'audiofolders', folder)
                        if path.exists(media_folder):
                            player.play(media_folder)
                            latest_id_file.write(
                                'The shortcut points to audiofolder %s.' % folder)
                    else:
                        open(shortcut, 'a').close()


context = deamon.DaemonContext(
    working_directory=WORKING_DIRECTORY,
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/RPI-jukebox-RFID.pid'),
    stdout=open(path.join(WORKING_DIRECTORY, 'logs', 'STDOUT'), 'w+'),
    stderr=open(path.join(WORKING_DIRECTORY, 'logs', 'STDERR'), 'w+'),
)

context.signal_map = {
    signal.SIGTERM: 'terminate',
    signal.SIGHUP: 'terminate',
}

with context:
    service = Service()
    service.main_loop()
