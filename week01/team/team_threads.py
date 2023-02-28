"""
Course: CSE 251
Lesson Week: 01 - Team Acvitiy
File: team.py
Author: Brother Comeau

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review team acvitiy details in I-Learn

"""
from datetime import datetime, timedelta
import threading


# Include cse 251 common Python files
from cse251 import *

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0


def thread_fun(start, end):
    global prime_count
    for i in range(start, end):
        if is_prime(i):
            prime_count += 1
            print(i, end=', ', flush=True)


def is_prime(n: int) -> bool:
    global numbers_processed
    numbers_processed += 1

    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    start = 10000000000
    range_count = 100000

    num_of_threads = 10
    threads = []
    range_of_threads = range_count // num_of_threads

# This creates threads and gives each one a range to test
    for i in range(10):
        thread_start = start + (range_of_threads * i)
        thread_end = thread_start + range_of_threads
        t = threading.Thread(
            target=thread_fun, args=(thread_start, thread_end))
        threads.append(t)

# start all threads
    for t in threads:
        t.start()

# wait for them to finish
    for t in threads:
        t.join()
    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    # TODO 3) change the program to divide the for loop into 10 threads

    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')
