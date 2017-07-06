import cv2
import numpy as np


class InVideo(object):
    def __init__(self, show_video=False):
        self.show_video = show_video
        if self.show_video:
            cv2.namedWindow('Video')
        self.capture = cv2.VideoCapture(0)

    def get_frame(self):
        _, frame = self.capture.read()
        if self.show_video:
            cv2.waitKey(1)
            cv2.imshow('Video', frame)
        return frame.tostring()

    def __del__(self):
        if self.show_video:
            cv2.destroyWindow('Video')


class OutVideo(object):
    def __init__(self):
        cv2.namedWindow('Video')

    def play_frame(self, frame):
        f = np.fromstring(bytes(frame), dtype=np.uint8).reshape((480, 640, 3))
        cv2.waitKey(1)
        cv2.imshow('Video', f)

    def __del__(self):
        cv2.destroyWindow('Video')
