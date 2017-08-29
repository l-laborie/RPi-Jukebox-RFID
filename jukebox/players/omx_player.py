# pylint: disable=unused-argument, no-self-use
from jukebox import MediaLister
from jukebox.players import Player
from jukebox.processors import OMXPlayerProcessor


class OMXPlayer(Player):
    def __init__(self, life_time=None):
        super(OMXPlayer, self).__init__(
            logging_name='OMXPlayer',
            processor=OMXPlayerProcessor(),
            media_lister=MediaLister(),
            life_time=life_time
        )
