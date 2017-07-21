#!/usr/bin/python

import threading
import time


exit_flag = 0


def print_time(thread_, counter, delay):
    while counter:
        if exit_flag:
            thread_.exit()
        time.sleep(delay)
        print '%s: %s' % (thread_.name, time.ctime(time.time()))
        counter -= 1


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        super(MyThread, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print 'Starting %s' % self.name
        print_time(self, self.counter, 5)
        print 'Exiting %s' % self.name


thread1 = MyThread(1, 'thread-1', 2)
thread2 = MyThread(1, 'thread-2', 4)


thread1.start()
thread2.start()


print 'Exiting main thread'
