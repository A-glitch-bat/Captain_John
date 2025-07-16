import time
import cv2
import numpy as np
import ctypes
import threading

class Mirror():
    def __init__(self):
        self.stop_event = None
        self.thread = None
        self.scale_factor = 2

        user32 = ctypes.windll.user32
        self.screensize = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    def irror(self, stat):
        """
        open mirror
        """
        if stat:
            self.stop_event = threading.Event()
            self.thread = threading.Thread(target=self.displayCamera)
            self.thread.start()
        else:
            self.stop_event.set()
            self.thread.join()
    # sub-function ^
    def displayCamera(self):
        # mirror function for threading
        stream = cv2.VideoCapture(0)
        cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

        if not stream.isOpened():
            print("Cannot open camera")
            return
        
        ret, frame = stream.read()
        if ret:
            frame = cv2.flip(frame, 1)
            new_size = (int(frame.shape[1] * self.scale_factor), int(frame.shape[0] * self.scale_factor))

            # center the mirror
            x = (self.screensize[0] - new_size[0]) // 2
            y = (self.screensize[1] - new_size[1]) // 2
            cv2.moveWindow("Webcam", x, y)

        while not self.stop_event.is_set():
            ret, frame = stream.read()
            if not ret:
                print("Stream closed")
                break

            frame = cv2.flip(frame, 1)
            resized_frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Webcam", resized_frame)

            if cv2.waitKey(1) == ord('q'):
                break
        stream.release()
        cv2.destroyAllWindows()

# Temporary main
if __name__ == "__main__":
    m = Mirror()
    m.irror(True)
    time.sleep(10)
    m.irror(False)
