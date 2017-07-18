# Forked from Francisco Sahli's https://github.com/fsahli/music-cards/blob/master/Reader.py

import os.path
import sys

from evdev import InputDevice, categorize, ecodes, list_devices
from select import select


class Reader(object):
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
        if not os.path.isfile(path + '/deviceName.txt'):
            sys.exit('Please run config.py first')
        else:
            with open(path + '/deviceName.txt', 'r') as f:
                device_name = f.read()
            devices = [InputDevice(fn) for fn in list_devices()]
            for device in devices:
                if device.name == device_name:
                    self.dev = device
                    break
            try:
                self.dev
            except Exception:
                sys.exit('Could not find the device %s\n. '
                         'Make sure is connected' % device_name)

    def read_card(self):
        result = ''
        key = ''
        while key != 'KEY_ENTER':
            _, _, _ = select([self.dev], [], [])
            for event in self.dev.read():
                if event.type == 1 and event.value == 1:
                    result += self.keys[event.code]
                    key = ecodes.KEY[event.code]
        return result[:-1]

