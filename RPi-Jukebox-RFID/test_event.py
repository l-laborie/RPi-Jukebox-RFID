#!/usr/bin/python

from threading import Thread, Event
import time


def wait_for_event(thread_name, event, timeout=None):
    event_is_set = event.wait(timeout)
    if event_is_set:
        print '%s detect event' % thread_name
    else:
        print 'timeout'


thread_names = [('thread-%d' % i, i == 2) for i in range(1, 3)]
threads = []
event = Event()

for thread_tuple in thread_names:
    thread_name, timeout = thread_tuple
    if timeout:
        thread = Thread(name=thread_name, target=wait_for_event, args=(thread_name, event, 4))
        threads.append(thread)
    else:
        thread = Thread(name=thread_name, target=wait_for_event, args=(thread_name, event,))
        threads.append(thread)
    thread.start()

time.sleep(3)
event.set()
