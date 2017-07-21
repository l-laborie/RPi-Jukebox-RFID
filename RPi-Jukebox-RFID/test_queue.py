#!/usr/bin/python

import Queue
import threading
import time


exit_flag = 0
queue_lock = threading.Lock()
work_queue = Queue.Queue(10)


def process_data(thread_name):
    while not exit_flag:
        queue_lock.acquire()
        if not work_queue.empty():
            data = work_queue.get()
            queue_lock.release()
            print '%s processing %s' % (thread_name, data)
        else:
            queue_lock.release()
        time.sleep(1)


class MyThread(threading.Thread):
    def __init__(self, thread_id, name):
        super(MyThread, self).__init__()
        self.thread_id = thread_id
        self.name = name

    def run(self):
        print 'Starting %s' % self.name
        process_data(self.name)
        print 'Exiting %s' % self.name


thread_names = [('thread-%d' % i, i) for i in range(1, 4)]
words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
         'nine', 'ten']
threads = []

for thread_desc in thread_names:
    name, id_ = thread_desc
    thread = MyThread(id_, name)
    thread.start()
    threads.append(thread)

queue_lock.acquire()
for word in words:
    work_queue.put(word)
queue_lock.release()

while not work_queue.empty():
    pass

exit_flag = 1

for t in threads:
    t.join()

print 'Exiting main thread'
