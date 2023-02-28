"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread/process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from queue import Queue

# Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1


def is_prime(n: int) -> bool:
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

# TODO create read_thread function


def read_thread(queue):
    with open('data.txt') as num:
        nums = num.readlines()
    for num in nums:
        queue.put(int(num))
    for _ in range(PRIME_PROCESS_COUNT):
        queue.put("END")

# TODO create prime_process function


def prime_process(queue, list):
    
    num = queue.get()
    while not num == "END":
        if is_prime(num):
            list 
            list.append(num)
        num = queue.get()


def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    # create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    nums = mp.Queue()
    # TODO Create shared data structures
    primes = mp.Manager().list()
    # TODO create reading thread
    read_thread(nums)
    # TODO create prime processes
    prime_process(nums, primes)
    # TODO Start them all

    # TODO wait for them to complete

    log.stop_timer(
        f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()
