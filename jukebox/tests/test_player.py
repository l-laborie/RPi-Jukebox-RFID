# pylint: disable=redefined-outer-name,unused-argument,protected-access
from os import path
from time import sleep
import pytest

from jukebox.players import Player


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
        file_name = path.split(args[0])[-1]
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


def test_quit(get_player):
    player = get_player()
    player.quit(wait=True)
    assert 'quit' in player._processor.result


def test_play_and_die_itself(work_directory, get_player):
    player = get_player()
    player.play(path.join(work_directory, 'media_test'))
    # life time of player
    sleep(2.5)
    assert player._processor.result == (
        'stop play (test.one) * * * * * play (test.two) * * * * * clean_up ')
    assert 'Start drive thread' in player.logged
    assert 'Start playing' in player.logged
    assert 'Execute stop action' in player.logged
    assert 'Execute play action' in player.logged
    assert 'Stop drive thread' in player.logged


def test_play_and_update_volume(work_directory, get_player):
    player = get_player()
    player.play(path.join(work_directory, 'media_test'))
    sleep(0.1)
    player.increase_volume()
    sleep(0.1)
    player.decrease_volume()
    sleep(0.1)
    player.quit(wait=True)
    assert 'vol +' in player._processor.result
    assert 'vol -' in player._processor.result


def test_player(work_directory, get_player):
    player = get_player()
    player.play(path.join(work_directory, 'media_test'))
    sleep(0.1)
    player.next_media()
    sleep(0.1)
    player.previous_media()
    sleep(0.1)
    player.quit(wait=True)
    assert player._processor.result.count('play (test.one)') == 2
    assert player._processor.result.count('play (test.two)') == 1


def test_stop(work_directory, get_player):
    player = get_player()
    player.play(path.join(work_directory, 'media_test'))
    sleep(0.5)
    player.stop()
    sleep(0.1)
    player.quit(wait=True)
    assert player._processor.result.startswith('stop play (test.one)')
    assert player._processor.result.endswith('stop stop quit clean_up ')
