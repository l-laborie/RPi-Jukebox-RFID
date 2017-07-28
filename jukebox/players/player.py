import logging
from threading import Thread, Event
import time

from jukebox import LockedQueue, LockedList, MediaLister


class Player(object):
    """Implement a mechanism to drive a player subprocess.

    Manage some features:
    - launch a process with a external program will read and play media files
    - manage playlist
    - manage some basic action:
        - next
        - previous
        - volume increase
        - volume decrease
        - stop
        - quit
    """

    _QUIT = 0
    _STOP = 1
    _PLAY = 2
    _INCREASE_VOL = 3
    _DECREASE_VOL = 4
    _CALLBACK = 5
    _ACTION_NAMES = ['quit', 'stop', 'play', 'vol +', 'vol -', 'callback']

    # Thread events
    _input_event = Event()
    _callback_event = Event()

    # Action queue manage
    _action_queue = LockedQueue(10)

    # Media file playlist mange
    _media_playlist = LockedList()

    # Driver
    _thread_drive = None
    _logger = None

    def process_cleanup(self):
        pass

    def process_is_state_change(self):
        pass

    def process_stop(self, *args):
        pass

    def process_play(self, *args):
        pass

    def process_increase_volume(self, *args):
        pass

    def process_decrease_volume(self, *args):
        pass

    def process_quit(self, *args):
        pass

    # pylint: disable=unused-argument
    def callback(self, *args):
        self._callback_event.set()
        return True

    def __init__(self, media_lister, life_time=None):
        self._thread_drive = Thread(target=self.__drive)
        self._thread_drive.start()
        self._process_by_action = {
            self._QUIT: self.process_quit,
            self._STOP: self.process_stop,
            self._PLAY: self.process_play,
            self._INCREASE_VOL: self.process_increase_volume,
            self._DECREASE_VOL: self.process_decrease_volume,
            self._CALLBACK: self.callback,
        }
        self._media_lister = media_lister or MediaLister()
        self._life_time = life_time

    def __log(self, level, message):
        if self._logger:
            self._logger.log(level, message)

    def __drive(self):
        self.__log(level=logging.INFO, message='Start drive thread')
        continue_ = True
        start_time = time.time()
        while continue_:
            if self._input_event.wait(0.05):
                while not self._action_queue.empty():
                    action = self._action_queue.pop()
                    self.__log(level=logging.DEBUG,
                               message='Execute %s action' %
                               self._ACTION_NAMES[action])
                    action = self._process_by_action.get(action)
                    if action:
                        continue_ &= action(self._media_playlist.get())
                self._input_event.clear()

            if self.process_is_state_change():
                if self._media_playlist.increase_index():
                    self._action_queue.push(self._PLAY)
                else:
                    self.process_cleanup()

            if self._life_time and continue_:
                life_time = time.time() - start_time
                continue_ = life_time < self._life_time

        life_time = time.time() - start_time
        self.__log(level=logging.INFO,
                   message='Stop drive thread. Life time : %fs' % life_time)

    def _set_actions(self, action_list, wait=False, timeout=None):
        if wait:
            action_list.append(self._CALLBACK)

        self._action_queue.push(*action_list)
        self._input_event.set()

        if wait:
            self._callback_event.wait(timeout=timeout)
            self._callback_event.clear()

    def stop(self, wait=False, timeout=None):
        self._media_playlist.set([])
        self._set_actions([self._STOP], wait=wait, timeout=timeout)

    def play(self, media_file, wait=False, timeout=None):
        media_files = self._media_lister.select_files(media_file)
        self._media_playlist.set(list(media_files))
        self.__log(level=logging.INFO,
                   message='Start playing %r' % media_files)
        self._set_actions([self._STOP, self._PLAY], wait=wait, timeout=timeout)

    def increase_volume(self, wait=False, timeout=None):
        self._set_actions([self._INCREASE_VOL], wait=wait, timeout=timeout)

    def decrease_volume(self, wait=False, timeout=None):
        self._set_actions([self._DECREASE_VOL], wait=wait, timeout=timeout)

    def next_media(self, wait=False, timeout=None):
        if self._media_playlist.increase_index():
            self._set_actions([self._STOP, self._PLAY], wait=wait,
                              timeout=timeout)

    def previous_media(self, wait=False, timeout=None):
        if self._media_playlist.decrease_index():
            self._set_actions([self._STOP, self._PLAY], wait=wait,
                              timeout=timeout)

    def quit(self, wait=False, timeout=None):
        self._set_actions([self._STOP, self._QUIT], wait=wait, timeout=timeout)
