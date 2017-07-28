# pylint: disable=redefined-outer-name
import pytest

from jukebox.players import Player


class DummyPlayer(Player):
    def __init__(self):
        self.result = ''
        super(DummyPlayer, self).__init__(media_lister=None, life_time=5)

    def process_cleanup(self):
        self.result += 'clean_up '
        return False

    def process_decrease_volume(self, *args):
        self.result += 'vol - '
        return True

    def process_increase_volume(self, *args):
        self.result += 'vol + '
        return True

    def process_is_state_change(self):
        if 'quit' in self.result:
            return True
        return None

    def process_play(self, *args):
        self.result += 'play %r ' % args
        return True

    def process_stop(self, *args):
        self.result += 'stop '
        return True

    def process_quit(self, *args):
        self.result += 'quit '
        return False


@pytest.fixture
def player():
    return DummyPlayer()


def test_quit(player):
    player.quit(wait=True)
    assert 'quit' in player.result
