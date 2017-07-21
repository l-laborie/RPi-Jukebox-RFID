#!/usr/bin/python

import threading
import time


thread_lock = threading.Lock()


def print_time(thread_name, counter, delay):
    while counter:
        time.sleep(delay)
        print '%s: %s' % (thread_name, time.ctime(time.time()))
        counter -= 1


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        super(MyThread, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print 'Starting %s' % self.name
        thread_lock.acquire()
        print_time(self.name, self.counter, 3)
        print 'Exiting %s' % self.name
        thread_lock.release()


thread1 = MyThread(1, 'thread-1', 2)
thread2 = MyThread(1, 'thread-2', 4)


thread1.start()
thread2.start()


threads = [thread1, thread2]

for t in threads:
    t.join()
print 'Exiting main thread'
