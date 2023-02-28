"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Roberto Reynoso

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

I would make a moving function to move if there is a spot open or not. Then from there in
the maze solve function I would make separate moves by thread if there is another direction
it can go, so that each thread can then have it's own direction to solve the maze.
Then lastly I would stop looking, once a thread finds the end.


Why would it work?

Each thread has a start and then an end this sequence then repeats itself until the maze is solved.

"""
import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False


def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def maze_move(position, color, maze, maze_lock):
    with maze_lock:
        if maze.can_move_here(position[0], position[1]):
            maze.move(position[0], position[1], color)
            return True
        return False


def maze_solve(position, color, maze, maze_lock, threads):
    global stop
    if stop or not maze_move(position, color, maze, maze_lock):
        return
    if maze.at_end(position[0], position[1]):
        print("end found")
        stop = True
        return
    while True:
        moves = maze.get_possible_moves(position[0], position[1])
        first_move = True
        for move in moves:
            if first_move:
                if stop:
                    return
                can_move = maze_move(move, color, maze, maze_lock)
                if can_move:
                    position = move
                    first_move = False
                    if maze.at_end(position[0], position[1]):
                        stop = True
                        return
            else:
                thread = threading.Thread(target=maze_solve, args=(
                    move, get_color(), maze, maze_lock, threads))
                thread.start()
                threads.append(thread)
        if first_move:
            return


def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global stop
    stop = False

    maze_lock = threading.Lock()
    threads = []
    thread = threading.Thread(target=maze_solve, args=(
        maze.get_start_pos(), get_color(), maze, maze_lock, threads))
    thread.start()
    threads.append(thread)
    for thread in threads:
        thread.join()
    global thread_count
    thread_count = len(threads)


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True


def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)


if __name__ == "__main__":
    main()
