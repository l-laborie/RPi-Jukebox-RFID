#!/usr/bin/python

from Queue import Queue
import subprocess
import sys
from threading import Thread, Event, Lock
from time import sleep

_LAUNCH_CMD = '/usr/bin/omxplayer'


class OMXPlayer(object):
    _LAUNCH_CMD = ['/usr/bin/omxplayer']
    _LAUNCH_CMD_ARGS = ['-s',  '--vol', '-4000']
    _PAUSE_CMD = 'p'
    _QUIT_CMD = 'q'
    _VOL_PLUS = '+'
    _VOL_MINUS = '-'

    _event = Event()

    _action_queue_lock = Lock()
    _media_file_lock = Lock()
    action_queue = Queue(10)

    _media_files = []
    _media_index = None

    _thread_drive = None
    _thread_process = None
    _process = None

    def __init__(self):
        self._thread_drive = Thread(target=self.__drive)
        self._thread_drive.start()

    def _set_media_files(self, value):
        self._media_file_lock.acquire()
        self._media_files = value
        self._media_index = 0 if len(self._media_files) > 0 else None
        self._media_file_lock.release()
        print('set media index to %r' % self._media_index)

    def _increase_index(self):
        old_index = self._media_index
        self._media_file_lock.acquire()
        if self._media_index is not None:
            self._media_index = min(len(self._media_files) -1, self._media_index + 1)
        self._media_file_lock.release()
        print('set media index to %r' % self._media_index)
        return self._media_index is not None and self._media_index > old_index

    def _decrease_index(self):
        old_index = self._media_index
        self._media_file_lock.acquire()
        if self._media_index is not None:
            self._media_index = max(0, self._media_index - 1)
        self._media_file_lock.release()
        print('set media index to %r' % self._media_index)
        return self._media_index is not None and self._media_index < old_index

    def _set_action(self, *actions):
        self._action_queue_lock.acquire()
        for action in actions:
            self.action_queue.put(action)
        self._action_queue_lock.release()

        self._event.set()

    @staticmethod
    def _select_files(path):
        import os
        result = []
        if os.path.isdir(path):
            for media in os.listdir(path):
                if media.lower().endswith(('.mp3', '.wav', '.flac')):
                    result.append(os.path.join(path, media))
            result.sort()
        else:
            result.append(path)
        return result

    def stop(self):
        self._set_media_files([])
        self._set_action('stop')

    def play(self, media_file):
        print(media_file)
        media_files = self._select_files(media_file)
        print(media_files)
        self._set_media_files(list(media_files))

        self._set_action('stop', 'play')

    def increase_volume(self):
        self._set_action('vol+')

    def decrease_volume(self):
        self._set_action('vol-')

    def next(self):
        if self._increase_index():
            self._set_action('stop', 'play')

    def previous(self):
        if self._decrease_index():
            self._set_action('stop', 'play')

    def __drive(self):
        print('start drive')
        while True:
            if self._event.wait(0.05):
                print('event seen')

                queue_is_empty = False
                while not queue_is_empty:
                    print('enter dequeue loop')
                    action = None

                    # get next action
                    self._action_queue_lock.acquire()
                    queue_is_empty = self.action_queue.empty()
                    if not queue_is_empty:
                        action = self.action_queue.get()
                    self._action_queue_lock.release()
                    print(action)

                    if action == 'stop' and self._process:
                        # proper stop and wit end
                        self._process.stdin.write(self._QUIT_CMD)
                        self._process.wait()

                    if action == 'play':
                        args = self._LAUNCH_CMD + [self._media_files[self._media_index],] + self._LAUNCH_CMD_ARGS
                        print(args)
                        self._process = subprocess.Popen(args, stdin = subprocess.PIPE, stdout = subprocess.PIPE,
                                                         stderr = subprocess.PIPE)

                    if action == 'vol+':
                        self._process.stdin.write(self._VOL_PLUS)

                    if action == 'vol-':
                        self._process.stdin.write(self._VOL_MINUS)

                self._event.clear()

            status = self._process.poll()
            if status is not None:
                print(status)
                if self._increase_index():
                    self._set_action('play')
                else:
                    break

            sleep(0.05)

        print('stop drive')


def play(path):
    print type(path)
    print path
    args = (_LAUNCH_CMD, '-s', str(path[0]), '--vol', '-2000')

    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sleep(5)

    process.stdin.write('+')
    sleep(5)
    process.stdin.write('+')
    sleep(5)
    process.stdin.write('+')
    sleep(5)
    process.stdin.write('+')

    while True:
        status = process.poll()
        if status is not None:
            break
        sleep(0.05)

    for line in process.stdout:
        print line


if __name__ == "__main__":
    # play(sys.argv[1:])
    player = OMXPlayer()
    print('call play')
    player.play('/home/pi/RPi-Jukebox-RFID/shared/audiofolders/Un_Monstre_a_Paris')
    sleep(10)
    player.stop()
    sleep(5)
    player.play('/home/pi/RPi-Jukebox-RFID/shared/audiofolders/M')
