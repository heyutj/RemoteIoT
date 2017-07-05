from mqtt_helper import MClient
from audio_helper import OutAudio
import cv2
import numpy as np



def show(frame):
    f = np.fromstring(bytes(frame), np.uint8)
    f = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.waitKey(10)
    cv2.imshow('Video', f)



mc = MClient()
oa = OutAudio()
cv2.namedWindow('Video')
mc.pub_sub([['remote/video', show, "subscribe"],['remote/audio', oa.playFrame, "subscribe"]])
cv2.destroyWindow('Video')
