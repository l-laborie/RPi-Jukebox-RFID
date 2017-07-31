from datetime import datetime
from os import path

from jukebox.players import OMXPlayer
from jukebox.setting import (
    WORKING_DIRECTORY,
    CMD_VOL_MINUS,
    CMD_STOP,
    CMD_SHUTDOWN,
    CMD_NEXT,
    CMD_PREVIOUS,
    CMD_VOL_PLUS,
)


class Handler(object):
    SHORTCUT = path.join(WORKING_DIRECTORY, 'shared', 'shortcuts')
    AUDIO_FOLDER = path.join(WORKING_DIRECTORY, 'shared', 'audiofolders')

    def __init__(self):
        self._player = OMXPlayer()
        self._commands = {
            CMD_SHUTDOWN: self._shutdown,
            CMD_STOP: self._player.stop,
            CMD_VOL_MINUS: self._player.decrease_volume,
            CMD_VOL_PLUS: self._player.increase_volume,
            CMD_NEXT: self._player.next_media,
            CMD_PREVIOUS: self._player.previous_media,
        }

    def _shutdown(self):
        pass

    def command(self, card_id):
        # check if the command is one of global
        action = self._commands.get(card_id)
        if action is not None:
            action()
            return

        # to be continue after this point
        latest_id_path = path.join(WORKING_DIRECTORY, 'shared',
                                   'latestID.txt')
        with open(latest_id_path, 'a') as ids_file:
            ids_file.write('Card ID %d was used at %s.' % (
                card_id, datetime.now().strftime()))

            shortcut = path.join(self.SHORTCUT, card_id)
            if path.isfile(shortcut):
                with open(shortcut, 'r') as content_file:
                    content = content_file.read()
                ids_file.write('This ID has been used before.')

                if content is not None:
                    media_folder = path.join(self.AUDIO_FOLDER, content)
                    self._player.play(media_folder)
                    return

            else:
                with open(shortcut, 'a') as shortcut_file:
                    shortcut_file.write(card_id)
                ids_file.write('This ID was used for the first time.')
