# pylint: disable=redefined-outer-name
from os import path
import pytest

from jukebox import MediaLister


@pytest.fixture
def work_directory():
    return path.dirname(path.realpath(__file__))


def test_media_lister_folder(work_directory):
    lister = MediaLister(media_extensions=('.one', '.two'))
    assert set(lister.select_files(
        path.join(work_directory, 'media_test')
    )) == {path.join(work_directory, 'media_test', 'test.one'),
           path.join(work_directory, 'media_test', 'test.two')}


def test_media_lister_file_correct_extension(work_directory):
    lister = MediaLister(media_extensions=('.one', '.two'))
    assert set(lister.select_files(
        path.join(work_directory, 'media_test', 'test.one')
    )) == {path.join(work_directory, 'media_test', 'test.one')}


def test_media_lister_file_incorrect_extension(work_directory):
    lister = MediaLister(media_extensions=('.one', '.two'))
    assert lister.select_files(
        path.join(work_directory, 'media_test', 'test.three')) == []
