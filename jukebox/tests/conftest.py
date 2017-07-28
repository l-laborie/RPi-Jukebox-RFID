from os import path
import pytest

from jukebox import MediaLister


@pytest.fixture
def work_directory():
    return path.dirname(path.realpath(__file__))


@pytest.fixture
def media_lister():
    return MediaLister(media_extensions=('.one', '.two'))
