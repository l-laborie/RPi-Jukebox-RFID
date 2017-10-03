# pylint: disable=redefined-outer-name
import pytest
from jukebox.processors import OMXPlayerProcessor


class FakeWrapper(object):
    def __init__(self, is_polled=None):
        self.actions_seen = []
        self.is_polled = is_polled

    def launch(self, args):
        self.actions_seen.append('launch(%r)' % args)

    def poll(self):
        self.actions_seen.append('poll()')
        return self.is_polled

    def wait(self):
        self.actions_seen.append('wait()')

    def write(self, command):
        self.actions_seen.append('write("%s")' % command)

    def clean_up(self):
        self.actions_seen.append('clean_up()')


@pytest.fixture
def wrapper():
    return FakeWrapper()


def get_player(wrapper):
    return OMXPlayerProcessor(wrapper=wrapper, default_volume=-2000,
                              command='command', args=['args'])


def test_play(wrapper):
    player = get_player(wrapper)
    player.process_play('one.mp3')

    assert wrapper.actions_seen == [
        "launch(['command', 'one.mp3', 'args', '--vol', '-2000'])"]


def test_clean_up(wrapper):
    player = get_player(wrapper)

    player.process_cleanup()
    assert wrapper.actions_seen == ['clean_up()']


def test_is_change():
    wrapper = FakeWrapper(is_polled=True)
    player = get_player(wrapper)

    assert player.process_is_state_change()
    assert wrapper.actions_seen == ['poll()']


def test_change_volume(wrapper):
    player = get_player(wrapper)
    player.process_increase_volume()
    player.process_play('one.mp3')
    player.process_decrease_volume()
    player.process_play('one.mp3')

    assert wrapper.actions_seen == [
        'write("+")',
        "launch(['command', 'one.mp3', 'args', '--vol', '-1950'])",
        'write("-")',
        "launch(['command', 'one.mp3', 'args', '--vol', '-2000'])",
    ]


def test_stop(wrapper):
    player = get_player(wrapper)
    player.process_stop()

    assert wrapper.actions_seen == ['write("q")', 'wait()']


def test_quit(wrapper):
    player = get_player(wrapper)
    assert not player.process_quit()
