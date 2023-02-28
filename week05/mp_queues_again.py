import multiprocessing
import queue

MAX_COUNT = 10


def write_function(q: queue.Queue):
    for i in range(MAX_COUNT):
        q.put(i)


def read_function(q: queue.Queue):
    for _ in range(MAX_COUNT):
        print(f"queue item = {q.get()}")


def main():
    # q = queue.Queue()
    q = multiprocessing.Manager().Queue()

    write = multiprocessing.Process(target=write_function, args=(q,))
    read = multiprocessing.Process(target=read_function, args=(q,))

    read.start()
    write.start()

    read.join()
    write.join()


if __name__ == "__main__":
    main()
