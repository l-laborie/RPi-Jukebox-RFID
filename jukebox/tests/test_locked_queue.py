from jukebox import LockedQueue


def test_push_one():
    queue = LockedQueue()

    assert not queue.pop()
    queue.push('one')
    assert queue.pop() == 'one'
    assert not queue.pop()


def test_push_two():
    queue = LockedQueue()

    assert not queue.pop()
    queue.push('one', 'two')
    assert queue.pop() == 'one'
    assert queue.pop() == 'two'
    assert not queue.pop()
