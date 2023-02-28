import multiprocessing as mp


def process_target(process_id, data):
    for i in range(10):
        data[process_id] += 1
    print(f"Process_{process_id}: {data}")


def main():

    # data = [0] * 3
    data = mp.Manager().list([0] * 3)

    processes = [mp.Process(target=process_target, args=(i, data))
                 for i in range(3)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print(f"All work completed: {sum(data)}")


if __name__ == "__main__":
    main()
