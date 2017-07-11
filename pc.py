from pyaudio import PyAudio, paInt16
import paho.mqtt.client as mqtt
import cv2
import logging
import numpy as np
logging.basicConfig(level=logging.DEBUG)


class Video(object):

    def play_frame(self, data):
        f = np.fromstring(bytes(data), dtype=np.uint8).reshape((480, 640, 3))
        logging.debug(np.shape(f))
        cv2.imshow('Video', f)
        logging.debug('show')
        cv2.waitKey(10)


class Audio(object):
    def __init__(self):
        self.SAMPLING_RATE = 8000
        self.p = PyAudio()
        self.stream = self.p.open(
            format=paInt16, channels=1, rate=self.SAMPLING_RATE, output=True)

    def play_frame(self, data):
        self.stream.write(bytes(data))


class PC(object):
    def __init__(self):
        self.video = Video()
        self.audio = Audio()

    def on_connect(self, client, userdata, flags, rc):
        topic = ["/IoT/video", "/IoT/audio"]
        for t in topic:
            mqttc.subscribe(t, 2)

    def on_message(self, client, userdata, message):
        logging.debug(message.topic)
        if message.topic == "/IoT/video":
            self.video.play_frame(message.payload)
        elif message.topic == "/IoT/audio":
            self.audio.play_frame(message.payload)


pc = PC()
mqttc = mqtt.Client()
mqttc.on_message = pc.on_message
mqttc.on_connect = pc.on_connect
mqttc.connect("127.0.0.1", port=1883, keepalive=60, bind_address="")
mqttc.loop_start()
# {"type":"ctrl","dev_type":"video","action":"on"}
while True:
    data = input()
    mqttc.publish('/IoT/ctrl', bytes(data, "utf-8"))
