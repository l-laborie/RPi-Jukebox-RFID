from os import path, listdir

from jukebox.setting import PLAYER_AVAILABLE_MEDIA_EXTENSIONS


class MediaLister(object):
    def __init__(self, media_extensions=None):
        self._media_extensions = (media_extensions or
                                  PLAYER_AVAILABLE_MEDIA_EXTENSIONS)

    def select_files(self, input_path):
        result = []
        if path.isdir(input_path):
            for media in listdir(input_path):
                if media.lower().endswith(self._media_extensions):
                    result.append(path.join(input_path, media))
            result.sort()
        elif path.isfile(input_path) and input_path.endswith(self._media_extensions):
            result.append(input_path)
        return result
