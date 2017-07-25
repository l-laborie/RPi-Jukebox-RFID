import logging
from Queue import Queue
import subprocess
from threading import Thread, Event, Lock
from time import sleep

from jukebox.setting import PLAYER_AVAILABLE_MEDIA_EXTENSIONS


LOGGER = logging.getLogger('OMXPlayer')


class OMXPlayer(object):
    _LAUNCH_CMD = ['/usr/bin/omxplayer']
    _LAUNCH_CMD_ARGS = ['-s',  '--vol', '-4000']
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

    def __init__(self, media_extensions=None):
        self._thread_drive = Thread(target=self.__drive)
        self._thread_drive.start()
        self.media_extensions = media_extensions or PLAYER_AVAILABLE_MEDIA_EXTENSIONS

    def _set_media_files(self, value):
        self._media_file_lock.acquire()
        self._media_files = value
        self._media_index = 0 if len(self._media_files) > 0 else None
        self._media_file_lock.release()
        LOGGER.debug('set media index to %r' % self._media_index)

    def _increase_index(self):
        old_index = self._media_index
        self._media_file_lock.acquire()
        if self._media_index is not None:
            self._media_index = min(
                len(self._media_files) - 1,
                self._media_index + 1)
        self._media_file_lock.release()
        LOGGER.debug('set media index to %r' % self._media_index)
        return self._media_index is not None and self._media_index > old_index

    def _decrease_index(self):
        old_index = self._media_index
        self._media_file_lock.acquire()
        if self._media_index is not None:
            self._media_index = max(0, self._media_index - 1)
        self._media_file_lock.release()
        LOGGER.debug('set media index to %r' % self._media_index)
        return self._media_index is not None and self._media_index < old_index

    def _set_action(self, *actions):
        self._action_queue_lock.acquire()
        for action in actions:
            self.action_queue.put(action)
        self._action_queue_lock.release()

        self._event.set()

    def _select_files(self, path):
        import os
        result = []
        if os.path.isdir(path):
            for media in os.listdir(path):
                if media.lower().endswith(self.media_extensions):
                    result.append(os.path.join(path, media))
            result.sort()
        else:
            result.append(path)
        return result

    def stop(self):
        self._set_media_files([])
        self._set_action('stop')

    def play(self, media_file):
        media_files = self._select_files(media_file)
        LOGGER.info('Start playing %r' % media_files)
        self._set_media_files(list(media_files))

        self._set_action('stop', 'play')

    def increase_volume(self):
        self._set_action('vol+')

    def decrease_volume(self):
        self._set_action('vol-')

    def next_media(self):
        if self._increase_index():
            self._set_action('stop', 'play')

    def previous_media(self):
        if self._decrease_index():
            self._set_action('stop', 'play')

    def quit(self):
        self._set_action('stop', 'quit')

    def __drive(self):
        LOGGER.debug('Start drive thread')
        _continue = True
        while _continue:
            if self._event.wait(0.05):
                queue_is_empty = False
                while not queue_is_empty:
                    action = None

                    # get next action
                    self._action_queue_lock.acquire()
                    queue_is_empty = self.action_queue.empty()
                    if not queue_is_empty:
                        action = self.action_queue.get()
                    self._action_queue_lock.release()
                    LOGGER.debug('Execute action %s' % action)

                    if action == 'stop' and self._process:
                        # proper stop and wit end
                        self._process.stdin.write(self._QUIT_CMD)
                        self._process.wait()

                    if action == 'play':
                        args = (
                            self._LAUNCH_CMD +
                            [self._media_files[self._media_index], ] +
                            self._LAUNCH_CMD_ARGS)
                        self._process = subprocess.Popen(
                            args,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )

                    if action == 'vol+':
                        self._process.stdin.write(self._VOL_PLUS)

                    if action == 'vol-':
                        self._process.stdin.write(self._VOL_MINUS)

                    if action == 'quit':
                        _continue = False

                self._event.clear()

            if self._process is not None:
                status = self._process.poll()
                if status is not None:
                    if self._increase_index():
                        self._set_action('play')
                    else:
                        self._process = None

            sleep(0.05)
            LOGGER.debug('Stop drive thread')
