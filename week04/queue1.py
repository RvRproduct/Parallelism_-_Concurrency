import queue

q = queue.Queue()

q.put("House")
q.put("tree")
q.put("Farm")
q.put("Truck")

print(f"Size of queue = {q.qsize()}")
print(f"Get an item from the queue: {q.get()}")


print(f"Size of queue = {q.qsize()}")
print(f"Get an item from the queue: {q.get()}")
