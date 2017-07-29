import logging
from os import path


# Config the working directory
WORKING_DIRECTORY = path.dirname(path.dirname(path.realpath(__file__)))


# Config player
PLAYER_AVAILABLE_MEDIA_EXTENSIONS = ('.mp3', '.wav', '.flac')
PLAYER_STARTUP_SOUND = path.join(WORKING_DIRECTORY, 'misc', 'startupsound.mp3')
PLAYER_HALT_SOUND = None

# Config OMXPlayer
OMXPLAYER_DEFAULT_VOLUME = -4000
OMXPLAYER_COMMAND = '/usr/bin/omxplayer'
OMXPLAYER_ARGS = ['-s']


# Config logging
LOGGING_LEVEL = logging.DEBUG
LOGGING_FILE = path.join(WORKING_DIRECTORY, 'logs', 'jukebox.log')


# Config card id for global actions
CMD_MUTE = 'mute'
CMD_VOL_PLUS = 'vol+'
CMD_VOL_MINUS = 'vol-'
CMD_NEXT = 'next'
CMD_PREVIOUS = 'previous'
CMD_STOP = 'stop'
CMD_SHUTDOWN = 'halt'
