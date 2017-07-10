import cv2
import numpy as np
import threading
import time


class InVideo(object):
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.capture = cv2.VideoCapture(device_id)
        self.capture.set(cv2.CV_CAP_PROP_FPS, 30)
        self.buffer = []

    def start(self):
        self.t = threading.Thread(target=self.record_frame)
        self.t.start()

    def record_frame(self):
        while True:
            print(len(self.buffer))
            time.sleep(0.05)
            _, frame = self.capture.read()
            self.buffer.append(frame)

    def stop(self):
        self.t.stop()
        self.buffer = []

    def get_frame(self):
        if self.buffer == []:
            return None
        else:
            return self.buffer.pop(0).tostring()


class OutVideo(object):
    def __init__(self):
        cv2.namedWindow('Video')

    def play_frame(self, frame):
        f = np.fromstring(bytes(frame), dtype=np.uint8).reshape((480, 640, 3))
        cv2.waitKey(1)
        cv2.imshow('Video', f)

    def __del__(self):
        cv2.destroyWindow('Video')
