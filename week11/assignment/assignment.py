"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
Roberto Reynoso
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE = 'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE = 'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'


def cleaner_waiting():
    time.sleep(random.uniform(0, 2))


def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))


def guest_waiting():
    time.sleep(random.uniform(0, 2))


def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))


def cleaner(id, cleaned, room_lock):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    # This starts a timer so that it can go as long as it is less than TIME (60 seconds)
    start_time = time.time()
    while start_time < TIME:
        # cleaner then waits to enter the room
        cleaner_waiting()
        # room is then cleaned while the room is locked
        with room_lock:
            print(STARTING_CLEANING_MESSAGE)
            # This then adds to how many rooms would be cleaned in the end
            cleaned.value += 1
            cleaner_cleaning(id)
            print(STOPPING_CLEANING_MESSAGE)


def guest(id, room_lock, guest_count, party_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    # This starts a timer and it will go as long as start time is less then TIME (60 seconds)
    start_time = time.time()
    guest_waiting()
    while start_time < TIME:
        # Using a Lock to check whether or not a guest can enter the room or not If the count is zero the party
        # the party then can start
        with room_lock:
            if guest_count.value == 0:
                print(STARTING_PARTY_MESSAGE)
                # This adds to the party count to see in the end how many parties are had
                party_count += 1
            # This will add to the guest count so that the party can stop and can then be reset
            # Then it repeats the process of guest waiting
            guest_count += 1
            guest_partying(id)
            if guest_count.value == 1:
                print(STOPPING_PARTY_MESSAGE)
        guest_count.value -= 1
        guest_waiting()


def main():
    # Start time of the running of the program.
    start_time = time.time()

    # These are the needed variables needed for the functions made above
    # We then pack the variables with default variables
    cleaned_count, party_count, guest_count = mp.Value(
        "i"), mp.Value("i"), mp.Value("i")
    cleaned_count.value, party_count.value, guest_count.value = 0, 0, 0

    # Here is the lock for the room when it is in use
    room_lock = mp.Lock()

    # This is the total amount of persons that will be attending whether it's a guest
    # or a cleaner
    total_persons = []

    # Then we will then go by the number of cleaning staff and Hotel Guests
    # The id will be the number of each guest or staff member.
    # We then make processes for the functions/actions will do and then append
    # The processes to a list
    for id in range(CLEANING_STAFF):
        total_persons.append(mp.Process(
            target=cleaner, args=(id, cleaned_count, room_lock)))

    for id in range(HOTEL_GUESTS):
        total_persons.append(mp.Process(target=guest, args=(
            id, room_lock, guest_count, party_count)))

    # we will then start each processes
    for person in total_persons:
        person.start()
    # we will wait for a process to complete to then move on
    for person in total_persons:
        person.join()

    # Results
    print(
        f'Room was cleaned {cleaned_count} times, there were {party_count} parties')


if __name__ == '__main__':
    main()
