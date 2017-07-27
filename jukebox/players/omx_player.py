# pylint: disable=unused-argument, no-self-use

import logging
import subprocess

from jukebox.players import Player


class OMXPlayer(Player):
    _LAUNCH_CMD = ['/usr/bin/omxplayer']
    _LAUNCH_CMD_ARGS = ['-s', '--vol', '-4000']

    _process = None

    _logger = logging.getLogger('OMXPlayer')

    def process_cleanup(self):
        self._process = None

    def process_is_state_change(self):
        if self._process is not None:
            return self._process.poll()

        return None

    def process_stop(self, *args):
        self._process.stdin.write('q')
        self._process.wait()
        return True

    def process_play(self, *args):
        args = (
            self._LAUNCH_CMD + [args[0]] + self._LAUNCH_CMD_ARGS)
        self._process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True

    def process_increase_volume(self, *args):
        self._process.stdin.write('+')
        return True

    def process_decrease_volume(self, *args):
        self._process.stdin.write('-')
        return True

    def process_quit(self, *args):
        return False
