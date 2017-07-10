import cv2
import numpy as np
import threading
import time


class InVideo(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.buffer = []
        self.video_frame = 0.04

    def start(self):
        self.record_frames()

    def record_frames(self):
        self.t = threading.Timer(self.video_frame, self.record_frame)
        self.t.start()

    def record_frame(self):
        print("rec_buffer"+str(len(self.buffer)))
        _, frame = self.capture.read()
        self.buffer.append(frame)
        self.t = threading.Timer(self.video_frame, self.record_frame)
        self.t.start()

    def stop(self):
        self.t.cancel()
        self.buffer = []

    def get_frame(self):
        print('out')
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
