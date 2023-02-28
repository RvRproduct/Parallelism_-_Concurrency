# importing the modules
from multiprocessing import Semaphore
import threading
import queue
import time
import random

MAX_THREADS = 4
ALL_DONE = "ALL_DONE"
MAX_QUEUE_SIZE = 20


def putter(q: queue.Queue, semMax: threading.Semaphore, senEmtpy: threading.Semaphore):
    with open("numbers.txt") as f:
        for line in f:

            semMax.acquire()

            print(f"size of queue {q.qsize()}")

            parts = line.split(",")
            number = int(parts[0])
            power = int(parts[1])

            q.put((number, power))
            time.sleep(random.uniform(0.001, 0.01))

    for _ in range(MAX_THREADS):
        q.put(ALL_DONE)


def getter(q: queue.Queue, semMax: threading.Semaphore, senEmtpy: threading.Semaphore):

    while True:

        pair = q.get()

        # Check if we are done
        if(pair == ALL_DONE):
            break

        number, power = pair

        print(f"{number}^{power} = {number ** power}\n")

        # Signal to the putter that the queue has an open slot.
        # If the putter is blocked because it doesn't want to
        # exceed the queue limit, then the putter will unblock
        # and add more to the queue.
        semMax.release()
        time.sleep(random.uniform(0.001, 0.01))


def main():

    # create a queue
    q = queue.Queue()

    # create a semephore with a counter starting at 20
    semMax = threading.Semaphore(MAX_QUEUE_SIZE)

    # create a binary semaphore (basically a lock)
    semEmpty = threading.Semaphore(0)

    # This tracks the max size of our queue

    # create a thread to put items onto the queue
    writer_thread = threading.Thread(target=putter, args=(q, semMax, semEmpty))

    # create a thread to read from the queue
    reader_thread = [threading.Thread(target=getter, args=(
        q, semMax, semEmpty)) for x in range(MAX_THREADS)]

    writer_thread.start()

    for t in reader_thread:
        t.start()


if __name__ == '__main__':
    main()
