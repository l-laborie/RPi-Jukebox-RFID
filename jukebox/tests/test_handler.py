import os
from jukebox.handlers import Handler


class Dummy(object):
    def __init__(self):
        self.seen = False

    def assert_true(self):
        self.seen = True

    def assert_played(self, folder):
        self.seen = 'tests/shared/audiofolders/audio' in folder


def test_handler_command(work_directory):
    shared = os.path.join(work_directory, 'shared')
    dummy = Dummy()

    handler = Handler(
        {'0': dummy.assert_true},
        shared,
        None
    )
    handler.command('0')
    assert dummy.seen


def test_handler_new_card(work_directory):
    shared = os.path.join(work_directory, 'shared')

    handler = Handler({}, shared, None)
    handler.command('0')

    assert os.path.exists(os.path.join(shared, 'shortcuts', '0'))
    assert open(os.path.join(shared, 'shortcuts', '0')).read() == '0'
    content = open(os.path.join(shared, 'latestID.txt')).read()
    assert "Card ID '0' was used at" in content
    assert "This ID was used for the first time." in content


def test_handler_existing_card(work_directory):
    shared = os.path.join(work_directory, 'shared')

    handler = Handler({}, shared, None)
    handler.command('1')

    assert os.path.exists(os.path.join(shared, 'shortcuts', '1'))
    assert open(os.path.join(shared, 'shortcuts', '1')).read() == '1'
    content = open(os.path.join(shared, 'latestID.txt')).read()
    assert "Card ID '1' was used at" in content
    assert "This ID has been used before." in content


def test_handler_audio(work_directory):
    shared = os.path.join(work_directory, 'shared')
    dummy = Dummy()

    handler = Handler({}, shared, dummy.assert_played)
    handler.command('2')

    assert os.path.exists(os.path.join(shared, 'shortcuts', '2'))
    assert open(os.path.join(shared, 'shortcuts', '2')).read() == 'audio'
    content = open(os.path.join(shared, 'latestID.txt')).read()
    assert dummy.seen
    assert "Card ID '2' was used at" in content
    assert "This ID has been used before." in content
