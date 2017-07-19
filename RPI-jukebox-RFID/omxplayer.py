from math import log10
import pexpect
import re
from threading import Thread, Event
from time import sleep


class OMXPlayer(object):
    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _SUBTITLE_REXP = re.compile(r"Subtitle count: (\d+), state: (\w+), index: (\d+), delay: (\d+)")
    _STATUS_REXP = re.compile(r"M:\d+ V:\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")

    _LAUNCH_CMD = '/usr/bin/omxplayer -s'
    _PAUSE_CMD = 'p'
    _QUIT_CMD = 'q'

    _VOLUMES_LEVEL = [(1.0, 0), (0.5, -1), (0.3, -2), (0.1, -3)]

    WAIT = 0
    RUNNING = 1

    def __init__(self):
        self.media_files = []
        self._process = None
        self.volume = 0.5
        self.position = None
        self.state = OMXPlayer.WAIT
        self.change_state = Event()
        self.pause = None
        self.list = []
        self.index = 0

        self._main_process = Thread(target=self._manager)
        self._main_process.start()

    def _compute_millibels(self):
        return 2000 * log10(self.volume)

    def _get_position(self):
        while True:
            index = self._process.expect([
                pexpect.TIMEOUT,
                pexpect.EOF,
                self._DONE_REXP,
                self._STATUS_REXP,
            ])

            if index == 0:
                self.state = OMXPlayer.RUNNING
                continue
            if index in (1, 2):
                self.state = OMXPlayer.WAIT
                self.change_state.set()
                break

            self.position = float(self._process.match.group(1))
            self.state = OMXPlayer.RUNNING
            sleep(0.05)

    def _play(self):
        # init volume
        volume_argument = '--vol %d' % self._compute_millibels()

        if self.index >= len(self.list):
            self.list = []
            self.index = 0
            return

        media_file = self.list[self.index]
        self.index = max(len(self.list), self.index + 1)

        cmd = ' '.join((self._LAUNCH_CMD, media_file, volume_argument))
        self._process = pexpect.spawn(cmd)

        self._AUDIOPROP_REXP.match(self._process.readline())
        self._SUBTITLE_REXP.match(self._process.readline())

        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()

        self.pause = False

    def _manager(self):
        print 'start'
        while self.change_state.is_set():
            print 'enter'
            self.change_state.clear()
            if self.list:
                self._play()

    def set_volume(self, volume):
        # assert 0 <= volume <= 1
        # self.volume =
        pass

    def play(self, *media_files):
        print 'play %r' % media_files
        self.list = media_files or []
        self.change_state.set()

    def pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.pause = not self.pause

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def next_media(self):
        self.stop()
        self._play()

    def previous_media(self):
        self.index = max(0, self.index -1)
        self.stop()
        self._play()
