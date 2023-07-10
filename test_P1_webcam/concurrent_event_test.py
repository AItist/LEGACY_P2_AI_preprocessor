import concurrent.futures
import random
import threading
import time
import queue

# Queue to hold the events
event_queue = queue.Queue()

def worker():
    while True:
        # Get the next event; this will block until an event is available
        event = event_queue.get()

        # Process the event
        print(f"Thread {threading.current_thread().name} got value: {event}")

        time.sleep(random.randint(1, 2))  # Sleep for a random interval between 1 and 10 seconds

        # Indicate that the processing is complete
        event_queue.task_done()

def event_updater():
    while True:
        # time.sleep(random.randint(1, 10))  # Sleep for a random interval between 1 and 10 seconds
        # time.sleep(0.2)  # Sleep for a random interval between 1 and 10 seconds

        # Update the queue with a new event
        event_queue.put(random.randint(1, 100))

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit worker tasks to the executor
    for _ in range(executor._max_workers):
        executor.submit(worker)

    # Run the event_updater in the main thread
    event_updater()
