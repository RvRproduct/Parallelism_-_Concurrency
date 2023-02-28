"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# Const Values
RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue


def retrieve_thread(info, log):  # TODO add arguments
    """ Process values from the data_queue """
    while True:
        # TODO check to see if anything is in the queue
        if info.empty():
            break

        # TODO process the value retrieved from the queue
        retrieved_value = info.get()

        # TODO make Internet call to get characters name and log it
        responses = requests.get(retrieved_value)
        data = responses.json()
        name = data["name"]
        log.write(f"name: {name}")


def file_reader(q, log):  # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "data.txt" and place items into a queue
    # with open("urls.txt") as data:
    #     urls = data.readlines()

    with open("urls.txt", "r") as urls:
        for line in urls:
            q.put(line.strip())
    print(urls)
    # for x in urls:
    #     q.put(x)

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    q.put(NO_MORE_VALUES)

    return q


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()

    # info = file_reader(q, log)
    # TODO create semaphore (if needed)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    threads = []
    file_thread = threading.Thread(target=file_reader, args=(q, log))
    for i in range(RETRIEVE_THREADS):
        r_thread = threading.Thread(target=retrieve_thread, args=(q, log))
        threads.append(r_thread)
    threads.append(file_reader)

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    # retrieve_thread(info, log)

    # TODO Wait for them to finish - The order doesn't matter

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()
