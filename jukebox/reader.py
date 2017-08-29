# Forked from Francisco Sahli's https://github.com/fsahli/music-cards/blob/master/Reader.py  # noqa
# pylint: disable=broad-except

import os.path
import sys

from select import select
# pylint: disable=import-error
from evdev import InputDevice, ecodes, list_devices


class EventDeviceWrapper(object):
    @staticmethod
    def get_devices():
        return [InputDevice(fn) for fn in list_devices()]

    @staticmethod
    def get_key(code):
        return ecodes.KEY[code]


class Reader(object):
    def __init__(self, event_device_wrapper=None):
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"  # noqa
        device_name_path = os.path.join(path, 'scripts', 'deviceName.txt')
        self._wrapper = event_device_wrapper or EventDeviceWrapper()
        if not os.path.isfile(device_name_path):
            sys.exit('Please run config.py first')
        else:
            with open(device_name_path, 'r') as device_name_file:
                device_name = device_name_file.read()
            for device in self._wrapper.get_devices():
                if device.name == device_name:
                    self.dev = device
                    break
            try:
                self.dev
            except Exception:
                sys.exit('Could not find the device %s\n. '
                         'Make sure is connected' % device_name)

    def read_card(self, timeout=None):
        result = ''
        key = ''
        while key != 'KEY_ENTER':
            dev, _, _ = select([self.dev], [], [], timeout=timeout)
            if not dev:
                # Timeout raised
                return None

            for event in self.dev.read():
                if event.type == 1 and event.value == 1:
                    result += self.keys[event.code]
                    key = self._wrapper.get_key(event.code)
        return result[:-1]
