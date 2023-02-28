import threading, queue
import time

THREADS = 4

def thread_function(q: queue.Queue, index):
    
    # This will block if the queue is empty
    item = q.get()
    print(f'Thread: {item}-{threading.current_thread()}')

def main():
    q = queue.Queue()

    q.put('one')
    q.put('two')
    q.put('three')

    # Create 4 threads - This is a list comprehension
    # Pass the queue as an argument to the threads
    #threads = [threading.Thread(target=thread_function, args=(q, i)) for i in range(THREADS)]
    threads = []
    for i in range(THREADS):
        threads.append(threading.Thread(target=thread_function, args=(q, i)))

    # start all threads
    for t in threads:
        t.start()

    time.sleep(6)
    q.put('LAST')

    # Wait for them to finish
    for t in threads:
        t.join()

    print('All work completed')


if __name__ == '__main__':
	main()