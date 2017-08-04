# pylint: disable=protected-access
from os import path
from time import sleep


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
