import threading
import queue
import time

MAX_COUNT = 10

def read_thread(shared_q):
    
    while True:
        obj = shared_q.get()
        print(f'GET {obj}')
        time.sleep(0.1)
        
        if(obj == "I'm done"):
            break

def write_thread(shared_q):
    
    for i in range(MAX_COUNT):
        # place value onto queue
        print(f'PUT: {i}')
        shared_q.put(i)
        
    time.sleep(5)
    
    print('\n----------\n')
    for i in range(MAX_COUNT, MAX_COUNT * 2, 1):
        # place value onto queue
        print(f'PUT: {i}')
        shared_q.put(i)
    
    # "signal" to the read thread that there is
    # nothing more to write. 
    shared_q.put("I'm done")

def main():
    shared_q = queue.Queue()

    write = threading.Thread(target=write_thread, args=(shared_q,))
    read = threading.Thread(target=read_thread, args=(shared_q,))

    read.start()        # Doesn't matter which starts first
    write.start()

    write.join()		# Order doesn't matter
    read.join()

    print('End')


if __name__ == '__main__':
    main()