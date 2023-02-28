from threading import Lock, Thread
import threading


def transfer(lock1, lock2):
    print(f'\n{threading.current_thread().name}, locking account one')
    lock1.acquire()

    print(f'\n{threading.current_thread().name}, locking account two')
    lock2.acquire()

    print(f'\n{threading.current_thread().name}, transfering money')

    print(f'\n{threading.current_thread().name}, release acount one')
    lock1.release()

    print(f'\n{threading.current_thread().name}, release acount two')
    lock2.release()


def transfer_do(lock1, lock2):

    # TODO - create a while loop and transfer money from one account to another,
    # (note: we won't actually be changing the balance and transferring anything,
    # just simulating locking each account)
    while True:

        # send money from first account to second
        transfer(lock_1, lock_2)

        # send money from second account to first
        transfer(lock_2, lock_1)


if __name__ == '__main__':

    # TODO create two locks
    lock_1 = threading.Lock()
    lock_2 = threading.Lock()

    # TODO - create 2 threads to transfer "money" from account one to account two.
    # range(1) 1 thread
    for x in range(2):
        t = Thread(target=transfer_do, args=(lock_1, lock_2))
        t.start()
