"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Roberto Reynoso
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

from fileinput import filename
import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'C:/Users/segan/OneDrive/Desktop/cse_251/cse251-course/week06/assignment/settings.txt'
BOXES_FILENAME = 'C:/Users/segan/OneDrive/Desktop/cse_251/cse251-course/week06/assignment/boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables


class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, marbles, pipe_enter, wait_time):
        mp.Process.__init__(self)
        self.marbles = marbles
        self.pipe_enter = pipe_enter
        self.wait_time = wait_time

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marbles):
            self.pipe_enter.send(random.choice(self.colors))
            time.sleep(self.wait_time)
        self.pipe_enter.send(None)
        self.pipe_enter.close()


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self, amount, pipe_end, pipe_enter, wait_time):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe_end = pipe_end
        self.pipe_enter = pipe_enter
        self.amount = amount
        self.wait_time = wait_time

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            marbles = Bag()
            while(marbles.get_size() < self.amount):
                marble = self.pipe_end.recv()
                if not marble:
                    self.pipe_end.close()
                    self.pipe_enter.send(None)
                    self.pipe_enter.close()
                    break
                marbles.add(marble)
            self.pipe_enter.send(marbles)
            time.sleep(self.wait_time)


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, pipe_end, pipe_enter, wait_time):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe_end = pipe_end
        self.pipe_enter = pipe_enter
        self.wait_time = wait_time

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            bag = self.pipe_end.recv()
            if not bag:
                self.pipe_end.close()
                self.pipe_enter.send(None)
                self.pipe_enter.close()
                break
            l_marble = random.choice(self.marble_names)
            gift = Gift(l_marble, bag)
            self.pipe_enter.send(gift)
            time.sleep(self.wait_time)


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """

    def __init__(self, gift_count, file, pipe_end, wait_time):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.file = file
        self.pipe_end = pipe_end
        self.wait_time = wait_time
        self.gift_count = gift_count

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.file, "w") as file:
            while True:
                gift = self.pipe_end.recv()
                if not gift:
                    self.pipe_exit.close()
                    break
                self.gift_count.value += 1
                now = datetime.now().time()
                file.write(f"Created - {now}: {gift}\n")
                time.sleep(self.wait_time)


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(
            f'The file {filename} doesn\'t exist.  No boxes were created.')


def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(
            f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    cb_pipe_enter, cb_pipe_end = mp.Pipe()
    ba_pipe_enter, ba_pipe_end = mp.Pipe()
    aw_pipe_enter, aw_pipe_end = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    gift_count = mp.Value("i")

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    processes = []

    processes.append(Marble_Creator(
        settings[MARBLE_COUNT], cb_pipe_enter, settings[CREATOR_DELAY]))
    processes.append(
        Bagger(settings[BAG_COUNT], cb_pipe_end, ba_pipe_enter, settings[BAGGER_DELAY]))
    processes.append(Assembler(ba_pipe_end, aw_pipe_enter,
                     settings[ASSEMBLER_DELAY]))
    processes.append(Wrapper(gift_count, BOXES_FILENAME,
                     aw_pipe_end, settings[WRAPPER_DELAY]))

    log.write('Starting the processes')
    # TODO add code here
    for process in processes:
        process.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    for process in processes:
        process.join()

    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    log.write(f"Created - {gift_count.value} gifts")


if __name__ == '__main__':
    main()
