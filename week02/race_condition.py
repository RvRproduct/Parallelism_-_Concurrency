from threading import Thread
import threading
from time import sleep


counter = 0


# TODO create an 'increase' function that increases the global
# variable by the value passed in. Create a local variable that
# is set equal to the global, change the local value, then
# assign the global to this final value.
def increase(value, lock: threading.Lock):
    global counter

    with lock:

        local_counter = counter
        print(
            f"\n{threading.current_thread().name} - BEFORE: global counter id = {id(counter)}")
        print(
            f"\n{threading.current_thread().name} - BEFORE: local counter id = {id(local_counter)}")

        local_counter += value

        sleep(0.1)

        print(
            f"\n{threading.current_thread().name} - AFTER: global counter id = {id(counter)}")
        print(
            f"\n{threading.current_thread().name} - AFTER: local counter id = {id(local_counter)}")

        counter = local_counter
        print(f"\n{threading.current_thread().name} - counter = {counter}")


# TODO - try without a lock first
lock = threading.Lock()

# create two threads
t1 = Thread(target=increase, args=(10, lock))
t2 = Thread(target=increase, args=(20, lock))

# start the threads
t1.start()
t2.start()


# wait for the threads to complete
t1.join()
t2.join()


print(f'The final counter is {counter}')
