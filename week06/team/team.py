"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp
import multiprocessing

# Include cse 251 common Python files
from cse251 import *


def sender(file, connection, counter):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(file, 'r') as text:
        data = text.readlines()
        for line in data:
            for word in line.split(" "):
                connection.send(word)
                counter += 1
        connection.send("NO MORE")
        connection.close()


def receiver(file, connection):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(file, 'w') as text:
        while True:
            word = connection.recv()
            if word == "NO MORE":
                connection.close()
                break
            elif word in ("\n"):
                text.write(word)
            else:
                text.write(word + " ")


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow=False)


def copy_file(log, filename1, filename2):
    # TODO create a pipe
    reciever_conn, sender_conn = multiprocessing.Pipe()

    # TODO create variable to count items sent over the pipe
    count_sent = 0

    # TODO create processes
    p1 = multiprocessing.Process(target=sender, args=(
        filename1, sender_conn, count_sent))
    p2 = multiprocessing.Process(
        target=receiver, args=(filename2, reciever_conn))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes
    p1.start()
    p2.start()

    # TODO wait for processes to finish
    p1.join()
    p2.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {p1}: ')
    log.write(f'items / second = {p2 / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__":

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')

    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')
