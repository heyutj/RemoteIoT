from mqtt_helper import MServer, MClient
from audio_helper import InAudio, OutAudio
import pygame
import pygame.camera
import time
import cv2
import struct

mc = MClient()

ia = InAudio()
cv2.namedWindow('Video')

capture = cv2.VideoCapture(0)
def getImg():
    _, frame = capture.read()
    cv2.waitKey(10)
    cv2.imshow('Video', frame)
    return cv2.imencode('.jpg', frame)[1].tostring()
mc.pub_sub([['remote/video', getImg, "publish"]])
