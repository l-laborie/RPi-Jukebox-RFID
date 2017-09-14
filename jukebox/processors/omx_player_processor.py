# pylint: disable=unused-argument, no-self-use
from jukebox.setting import (
    OMXPLAYER_ARGS,
    OMXPLAYER_COMMAND,
    OMXPLAYER_DEFAULT_VOLUME,
)
from jukebox.wrappers import ProcessWrapper


class OMXPlayerProcessor(object):
    def __init__(self, wrapper=None, default_volume=None, command=None,
                 args=None):
        self._args = args or OMXPLAYER_ARGS
        self._command = command or OMXPLAYER_COMMAND
        self._default_volume = default_volume or OMXPLAYER_DEFAULT_VOLUME
        self._current_volume = self._default_volume
        self._wrapper = wrapper or ProcessWrapper()

    def process_cleanup(self):
        self._wrapper.clean_up()

    def process_is_state_change(self):
        return self._wrapper.poll()

    def process_stop(self, *args):
        self._wrapper.write('q')
        self._wrapper.wait()
        return True

    def process_play(self, *args):
        launch_args = (
            [self._command, args[0]] + self._args +
            ['--vol', str(self._default_volume)])
        self._wrapper.launch(launch_args)
        return True

    def process_increase_volume(self, *args):
        new_volume = min(0, self._current_volume + 50)
        if new_volume != self._current_volume:
            self._wrapper.write('+')
            self._current_volume = new_volume
        return True

    def process_decrease_volume(self, *args):
        print 'volume: %r' % self._current_volume
        new_volume = max(-6000, self._current_volume - 50)
        if new_volume != self._current_volume:
            self._wrapper.write('-')
            self._current_volume = new_volume
        return True

    def process_quit(self, *args):
        return False
