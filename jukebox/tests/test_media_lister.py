# pylint: disable=redefined-outer-name
from os import path


def test_media_lister_folder(work_directory, media_lister):
    assert set(media_lister.select_files(
        path.join(work_directory, 'media_test')
    )) == {
        path.join(work_directory, 'media_test', 'test.one'),
        path.join(work_directory, 'media_test', 'test.two')}


def test_media_lister_file_correct_extension(work_directory, media_lister):
    assert set(media_lister.select_files(
        path.join(work_directory, 'media_test', 'test.one')
    )) == {path.join(work_directory, 'media_test', 'test.one')}


def test_media_lister_file_incorrect_extension(work_directory, media_lister):
    assert media_lister.select_files(
        path.join(work_directory, 'media_test', 'test.three')) == []


def test_media_lister_not_a_file(work_directory, media_lister):
    assert media_lister.select_files(
        path.join(work_directory, 'media_test', 'test.four')) == []
