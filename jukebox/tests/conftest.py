# pylint: disable=redefined-outer-name,unused-argument
import os
import pytest

from jukebox import MediaLister
from jukebox.players import Player


@pytest.fixture
def work_directory():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def media_lister():
    return MediaLister(media_extensions=('.one', '.two'))


def pytest_runtest_teardown():
    base_directory = os.path.dirname(os.path.realpath(__file__))
    shared = os.path.join(base_directory, 'shared')
    if os.path.exists(os.path.join(shared, 'shortcuts', '0')):
        os.remove(os.path.join(shared, 'shortcuts', '0'))
    if os.path.exists(os.path.join(shared, 'latestID.txt')):
        os.remove(os.path.join(shared, 'latestID.txt'))


class DummyProcessor(object):
    def __init__(self):
        self.result = ''
        self.running = False

    def process_cleanup(self):
        self.result += 'clean_up '

    def process_is_state_change(self):
        if 'quit' in self.result:
            # emulate that the player make exit code
            return True

        if self.result.endswith(('play (test.one) ', 'play (test.two) ')):
            # Simulate the play a media start and stop in the same loop
            self.result += '* '
            self.running = True
            return None

        if self.result.endswith('* * * * * '):
            # simulate one loop are spent to play media
            self.running = False
            return True

        if self.running:
            self.result += '* '
        return None

    def process_stop(self, *args):
        self.running = False
        self.result += 'stop '
        return True

    def process_play(self, *args):
        file_name = os.path.split(args[0])[-1]
        self.result += 'play (%s) ' % file_name
        return True

    def process_increase_volume(self, *args):
        self.result += 'vol + '
        return True

    def process_decrease_volume(self, *args):
        self.result += 'vol - '
        return True

    def process_quit(self, *args):
        self.result += 'quit '
        return False


class DummyPlayer(Player):
    logged = ''

    class DummyLogger(object):
        @staticmethod
        # pylint: disable=unused-argument
        def log(level, message):
            DummyPlayer.logged += '%s ' % message

    def __init__(self, logging_name, wrapper, media_lister, life_time=None):
        self._logger = DummyPlayer.DummyLogger()
        super(DummyPlayer, self).__init__(logging_name, wrapper,
                                          media_lister, life_time)


@pytest.fixture
def get_player(media_lister):
    return lambda: DummyPlayer('dummy', DummyProcessor(), media_lister, 2)
