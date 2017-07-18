import deamon
import lockfile
import os
import signal


def init():
    pass


def main_loop():
    pass


WORKING_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))

context = deamon.DaemonContext(
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

init()

with context:
    main_loop()
