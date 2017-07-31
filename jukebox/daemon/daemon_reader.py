import daemon
import lockfile
import os
import signal
from sys import path
path.append(os.getcwd())

from jukebox.reader import Reader
from jukebox.handlers import Handler


WORKING_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))

context = daemon.DaemonContext(
    working_directory=WORKING_DIRECTORY,
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/RPI-jukebox-RFID.pid'),
    stdout=open(os.path.join(WORKING_DIRECTORY, 'logs', 'STDOUT'), 'w+'),
    stderr=open(os.path.join(WORKING_DIRECTORY, 'logs', 'STDERR'), 'w+'),
)

context.signal_map = {
    signal.SIGTERM: 'terminate',
    signal.SIGHUP: 'terminate',
}

# init
reader = Reader()
handler = Handler()

# main
with context:
    while True:
        card_id = reader.read_card()
        handler.command(card_id)
