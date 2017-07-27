import pytest
from jukebox import LockedList


def test_empty_list():
    list_ = LockedList()

    assert list_.get() is None
    assert not list_.increase_index()
    assert not list_.decrease_index()


def test_one_element_list():
    list_ = LockedList(data=['one'])

    assert list_.get() == 'one'
    assert not list_.increase_index()
    assert not list_.decrease_index()


def test_two_element_list():
    list_ = LockedList(data=['one', 'two'])

    assert list_.get() == 'one'
    assert list_.increase_index()
    assert list_.get() == 'two'
    assert not list_.increase_index()
    assert list_.decrease_index()
    assert list_.get() == 'one'
    assert not list_.decrease_index()


def test_set_list():
    list_ = LockedList()

    list_.set(['one'])
    assert list_.get() == 'one'
    assert not list_.increase_index()
    assert not list_.decrease_index()

    list_.set(['one', 'two'])
    assert list_.get() == 'one'
    assert list_.increase_index()
    assert list_.get() == 'two'
    assert not list_.increase_index()
    assert list_.decrease_index()
    assert list_.get() == 'one'
    assert not list_.decrease_index()


# pylint: disable=unused-variable
def test_wrong_assignment():
    with pytest.raises(AssertionError):
        list_ = LockedList('one')
    with pytest.raises(AssertionError):
        list_ = LockedList(1)
    with pytest.raises(AssertionError):
        list_ = LockedList(('one',))
    with pytest.raises(AssertionError):
        list_ = LockedList(object())
