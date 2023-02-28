# importing the modules
from multiprocessing import Semaphore
import threading       
import time        

THREADS = 2
SEMAPHORE_COUNT = 3

# creating instance
def display(semaphore: Semaphore, name):
    
    # calling acquire method
    
    print(f'Thread-{name} value before acquire = {semaphore._value}\n')
    semaphore.acquire()                
    print(f'Thread-{name} value after acquire = {semaphore._value}\n')

    time.sleep(1)
        
    # calling release method
    semaphore.release()    
    print(f'Thread-{name} value after release = {semaphore._value}\n')

def increment(semaphore: Semaphore):
    semaphore.release()


def main():
    sem = threading.Semaphore(0)        

    # creating multiple thread 
    threads = [ threading.Thread(target=display, args=(sem, f'{x}')) for x in range(1, THREADS + 1) ]
    threads.append(threading.Thread(target=increment, args=(sem,)))
  
    # calling the threads 
    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()