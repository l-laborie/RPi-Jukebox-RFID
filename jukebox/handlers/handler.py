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
    def __init__(self, commands, path_shared, play):
        self._commands = commands
        self._path_shared = path_shared
        self._path_shortcut = path.join(path_shared, 'shortcuts')
        self._path_audio_folder = path.join(path_shared, 'audiofolders')
        self._play = play

    def command(self, card_id):
        # check if the command is one of global
        action = self._commands.get(card_id)
        if action is not None:
            action()
            return

        # to be continue after this point
        latest_id_path = path.join(self._path_shared, 'latestID.txt')
        with open(latest_id_path, 'a') as ids_file:
            ids_file.write('Card ID %r was used at %s.' % (
                card_id, datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')))

            shortcut = path.join(self._path_shortcut, card_id)
            if path.isfile(shortcut):
                with open(shortcut, 'r') as content_file:
                    content = content_file.read()
                ids_file.write('This ID has been used before.')

                if content is not None and content != card_id:
                    media_folder = path.join(self._path_audio_folder, content)
                    self._play(media_folder)
                    return

            else:
                with open(shortcut, 'a') as shortcut_file:
                    shortcut_file.write(card_id)
                ids_file.write('This ID was used for the first time.')


def handler_factory(player=None, **extra_actions):
    player = player or OMXPlayer()
    commands = {
        CMD_STOP: player.stop,
        CMD_VOL_MINUS: player.decrease_volume,
        CMD_VOL_PLUS: player.increase_volume,
        CMD_NEXT: player.next_media,
        CMD_PREVIOUS: player.previous_media,
    }
    if CMD_SHUTDOWN not in extra_actions:
        from subprocess import call
        extra_actions[CMD_SHUTDOWN] = call('sudo poweroff', shell=True)
    commands.update(extra_actions)

    shared = path.join(WORKING_DIRECTORY, 'shared')
    return Handler(commands, shared, player.play)
