import threading

VALUES_TO_ADD = 1000
NUM_OF_THREADS = 3


def thread_function(thread_id, data):
    for i in range(VALUES_TO_ADD):
        data[thread_id] += 1
    print(f"Thread_{thread_id}: {data}")


def main():
    data = [0] * NUM_OF_THREADS

    threads = [threading.Thread(target=thread_function, args=(
        i, data)) for i in range(NUM_OF_THREADS)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"All work completedd {sum(data)}")


if __name__ == "__main__":
    main()
