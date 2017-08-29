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


def shutdown():
    from subprocess import call
    call('sudo poweroff', shell=True)


def _create_gracefully_shutdown(player=None, terminate_timeout=None,
                                shutdown_action=None):
    shutdown_action = shutdown_action or shutdown

    if not player:
        return shutdown_action

    def _shutdown():
        player.quit(wait=True, timeout=terminate_timeout)
        shutdown_action()

    return _shutdown


def handler_factory(player=None, terminate_timeout=None, **extra_actions):
    player = player or OMXPlayer()
    commands = {
        CMD_STOP: player.stop,
        CMD_VOL_MINUS: player.decrease_volume,
        CMD_VOL_PLUS: player.increase_volume,
        CMD_NEXT: player.next_media,
        CMD_PREVIOUS: player.previous_media,
    }
    shutdown_action = extra_actions.pop(CMD_SHUTDOWN, shutdown)
    commands[CMD_SHUTDOWN] = _create_gracefully_shutdown(
        player=player, terminate_timeout=terminate_timeout,
        shutdown_action=shutdown_action
    )
    commands.update(extra_actions)

    shared = path.join(WORKING_DIRECTORY, 'shared')
    return Handler(commands, shared, player.play)
