import os
import pytest

from jukebox import MediaLister


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
