from multiprocessing import Process, Array, Value, Queue, Lock
import cv2
import numpy as np
import time

# import multiprocessing import profile

def capture_image(shared_array, size, lock, index):
    cap = cv2.VideoCapture(index)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Write the gray image to shared memory
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        with lock:
            shared_array[:len(img_bytes)] = np.frombuffer(img_bytes, dtype='uint8')
            size.value = len(img_bytes)

        time.sleep(0.1)

    # When everything done, release the capture
    cap.release()

def process_image(shared_array, size, lock, queue):
    while True:
        with lock:
            img_bytes = bytes(shared_array[:size.value])  # only read the number of bytes that were written

        if img_bytes:
            img_np = np.frombuffer(img_bytes, dtype='uint8')
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            # Now img is a grayscale OpenCV image
            # Do processing here...

            # Instead of showing the image here, we put it on the queue
            queue.put(img)

        time.sleep(0.1)


def display_image(queue):
    while True:
        img = queue.get()  # Get image from queue
        if img is not None:
            # cv2.imwrite('test.jpg', img)
            cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if Q is pressed
            break

if __name__ == '__main__':
    # Maximum size for a JPEG image in bytes
    max_size = 1024 * 1024 * 3
    index = 0

    lock = Lock()
    shared_array = Array('B', max_size)
    size = Value('i', 0)
    queue = Queue()  # Queue for images

    p1 = Process(target=capture_image, args=(shared_array, size, lock, index))
    p2 = Process(target=process_image, args=(shared_array, size, lock, queue))

    p1.start()
    p2.start()

    # In the main process, we display the images
    display_image(queue)

    p1.join()
    p2.join()
