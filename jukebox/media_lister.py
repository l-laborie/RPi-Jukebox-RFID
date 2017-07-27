from os import path, listdir

from jukebox.setting import PLAYER_AVAILABLE_MEDIA_EXTENSIONS


class MediaLister(object):
    def __init__(self, media_extensions):
        self._media_extensions = (media_extensions or
                                  PLAYER_AVAILABLE_MEDIA_EXTENSIONS)

    def select_files(self, input_path):
        result = []
        if path.isdir(input_path):
            for media in listdir(input_path):
                if media.lower().endswith(self._media_extensions):
                    result.append(path.join(path, media))
            result.sort()
        else:
            result.append(path)
        return result
