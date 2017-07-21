#!/usr/bin/python

from math import log10
import pexpect
import re
import Queue
from threading import Thread, Event, Lock
from time import sleep


class OMXPlayer(object):

    class PlayerAction(object):
        def __init__(self, name):
            self.name = name

    class PlayerState(object):
        def __init__(self, name):
            self.name = name

    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _SUBTITLE_REXP = re.compile(r"Subtitle count: (\d+), state: (\w+), index: (\d+), delay: (\d+)")
    _STATUS_REXP = re.compile(r"M:\d+ V:\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")

    _LAUNCH_CMD = '/usr/bin/omxplayer -s'
    _PAUSE_CMD = 'p'
    _QUIT_CMD = 'q'

    ACTION_STOP = PlayerAction('stop')
    ACTION_PAUSE = PlayerAction('pause')
    ACTION_NEXT = PlayerAction('next')
    ACTION_PREVIOUS = PlayerAction('previous')
    ACTION_PLAY = PlayerAction('play')

    STATE_STOP = PlayerAction('stop')
    STATE_PAUSE = PlayerAction('pause')
    STATE_PLAY = PlayerAction('play')

    _event = Event()
    state = STATE_STOP

    _action_queue_lock = Lock()
    _media_file_lock = Lock()
    action_queue = Queue.Queue(10)

    _media_files = []
    _media_index = None

    _thread_drive = None
    _thread_process = None
    _process = None

    def __init__(self):
        self._thread_drive = Thread(target=self._drive)
        self._thread_drive.start()

    def _clean_up(self):
        return True

    def clean_up(self):
        self._set_action(self._clean_up)
        self._thread_drive.join()

    def _set_media_files(self, value):
        self._media_file_lock.acquire()
        self._media_files = value
        self._media_index = 0 if len(self._media_files) > 0 else None
        self._media_file_lock.release()

    def _set_action(self, action):
        self._action_queue_lock.acquire()
        self.action_queue.put(action)
        self._action_queue_lock.release()

        self._event.set()

    def _play(self):
        print('start play')

        self._kill()

        if self._media_index >= len(self._media_files):
            self._set_media_files([])
            return

        media_file = self._media_files[self._media_index]

        cmd = ' '.join((self._LAUNCH_CMD, media_file))
        self._process = pexpect.spawn(cmd)

        self._AUDIOPROP_REXP.match(self._process.readline())
        self._SUBTITLE_REXP.match(self._process.readline())

        self._thread_process = Thread(target=self._get_position)
        self._thread_process.start()

        print('end play')

    def play(self, *media_files):
        self._set_media_files(list(media_files))

        self._set_action(self._play)

    def _pause(self):
        if self.state == OMXPlayer.STATE_PLAY:
            self.state = OMXPlayer.STATE_PAUSE
        else:
            self.state = OMXPlayer.STATE_PLAY

        self._process.send(self._PAUSE_CMD)

    def pause(self):
        self._set_action(self._pause())

    def _kill(self):
        print('enter kill')
        if self._process:
            self._process.send(self._QUIT_CMD)
            # wait old thread process is end

        if self._thread_process:
            self._thread_process.join()
            self._thread_process = None

        print('end kill')

    def _stop(self):
        self._set_media_files([])

        self._kill()

    def stop(self):
        self._set_action(self._stop)

    def _next(self):
        max_media_index = len(self._media_files) - 1
        if max_media_index == 0:
            return

        self._stop()
        new_index = min(max_media_index, self._media_index + 1)
        if self._media_index <= new_index:
            # the next called by the last media file --> turn off
            return

        self._media_index = new_index
        self._play()

    def next_media(self):
        self._set_action(self._next)

    def _previous(self):
        if len(self._media_files) == 0:
            return

        new_index = max(0, self._media_index - 1)
        if self._media_index >= new_index:
            return

        self._media_index = new_index
        self._stop()
        self._play()

    def previous_media(self):
        self._set_action(self._previous)

    def _drive(self):
        print('start drive')
        while self._event.wait():
            print('enter main loop')
            queue_is_empty = False
            while not queue_is_empty:
                print('enter dequeue loop')
                self._action_queue_lock.acquire()
                queue_is_empty = self.action_queue.empty()
                if not queue_is_empty:
                    action = self.action_queue.get()
                self._action_queue_lock.release()

                if action():
                    print('end drive')
                    return

            self._event.clear()

    def _get_position(self):
        print('start get position')
        while True:
            index = self._process.expect([
                pexpect.TIMEOUT,
                pexpect.EOF,
                self._DONE_REXP,
                self._STATUS_REXP,
            ])
            print(index)
            # if index == 0:
            if index in (0, 1):
                print('--> timeout')
                if self.state == OMXPlayer.STATE_STOP:
                    self.state = OMXPlayer.STATE_PLAY
                continue
            # if index in (1, 2):
            if index == 1:
                print('--> stop')
                self.state = OMXPlayer.STATE_STOP
                self._process.terminate(force=True)
                self._process = None
                break

            print('--> run')
            # self.position = float(self._process.match.group(1))
            if self.state == OMXPlayer.STATE_STOP:
                self.state = OMXPlayer.STATE_PLAY
            sleep(0.05)

        self.next_media()

player = OMXPlayer()
mojo = '/home/pi/RPi-Jukebox-RFID/misc/startupsound.mp3'
