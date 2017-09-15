import logging
from os import path


# The working directory Config
WORKING_DIRECTORY = path.dirname(path.dirname(path.realpath(__file__)))


# player Config
PLAYER_AVAILABLE_MEDIA_EXTENSIONS = ('.mp3', '.wav', '.flac', 'wma')
PLAYER_STARTUP_SOUND = path.join(WORKING_DIRECTORY, 'misc', 'startupsound.mp3')
PLAYER_HALT_SOUND = None

# OMXPlayer Config
OMXPLAYER_DEFAULT_VOLUME = -2000
OMXPLAYER_COMMAND = '/usr/bin/omxplayer'
OMXPLAYER_ARGS = ['-s']

# Logging Config
LOGGING_LEVEL = logging.DEBUG
LOGGING_FOLDER = path.join(WORKING_DIRECTORY, 'logs')

# Config card id for global actions
CMD_MUTE = 'mute'
CMD_VOL_PLUS = 'vol+'
CMD_VOL_MINUS = 'vol-'
CMD_NEXT = 'next'
CMD_PREVIOUS = 'previous'
CMD_STOP = 'stop'
CMD_SHUTDOWN = 'halt'

# Daemon Config
DAEMON_MAIN_LOOP_TIMEOUT = 0.5  # in second maximum time spend in each loop
