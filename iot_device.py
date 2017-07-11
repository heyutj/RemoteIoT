import paho.mqtt.client as mqtt
import threading
import logging
import json
import cv2
from pyaudio import PyAudio, paInt16
import numpy as np
import wave
logging.basicConfig(level=logging.DEBUG)


class Video(object):
    def __init__(self):
        self.buffer = []
        self.video_frame = 0.04
        self.send_frame = 0.04
        self.should_stop_rec = True
        self.should_stop_pub = True

    def start_rec(self):
        self.should_stop_rec = False
        self.capture = cv2.VideoCapture(0)
        logging.info('video start rec')
        self.t1 = threading.Timer(self.video_frame, self.record)
        self.t1.start()

    def record(self):
        logging.debug('video recing')
        _, frame = self.capture.read()
        logging.debug('video rec1:' + str(len(self.buffer)))
        self.buffer.append(frame)
        logging.debug('video rec2:' + str(len(self.buffer)))
        if not self.should_stop_rec:
            self.t1 = threading.Timer(self.video_frame, self.record)
            self.t1.start()

    def stop_rec(self):
        self.should_stop_rec = True
        self.t1.cancel()
        self.buffer = []
        del self.capture

    def start_pub(self, client):
        self.should_stop_pub = False
        logging.info('video start pub')
        self.t2 = threading.Timer(
            self.send_frame, self.publish, args=(client,))
        self.t2.start()

    def publish(self, client):
        logging.debug("video buffer:" + str(len(self.buffer)))
        if self.buffer != []:
            logging.debug('video pubing')
            data = self.buffer.pop(0).tostring()
            client.publish(topic='/IoT/video', payload=data)
            logging.debug('video pubbed')
        if not self.should_stop_pub:
            self.t2 = threading.Timer(
                self.send_frame, self.publish, args=(client,))
            self.t2.start()

    def stop_pub(self):
        logging.info('video stop pub')
        self.should_stop_pub = True
        self.t2.cancel()


class Audio(object):
    def __init__(self):
        self.NUM_SAMPLES = 2000
        self.SAMPLING_RATE = 8000
        p = PyAudio()
        self.stream = p.open(format=paInt16, channels=1,
                             rate=self.SAMPLING_RATE,
                             input=True, frames_per_buffer=self.NUM_SAMPLES)
        self.buffer = []
        self.audio_frame = 0.25
        self.send_frame = 0.25
        self.should_stop_rec = True
        self.should_stop_pub = True

    def start_rec(self):
        self.should_stop_rec = False
        logging.info('audio start rec')
        self.t1 = threading.Timer(self.audio_frame, self.record)
        self.t1.start()

    def record(self):
        logging.debug('audio recing')
        logging.debug('audio rec1:' + str(len(self.buffer)))
        self.buffer.append(self.stream.read(self.NUM_SAMPLES))
        logging.debug('audio rec2:' + str(len(self.buffer)))
        if not self.should_stop_rec:
            self.t1 = threading.Timer(self.audio_frame, self.record)
            self.t1.start()

    def stop_rec(self):
        self.should_stop_rec = True
        logging.info('audio stop rec')
        self.t1.cancel()
        self.buffer = []

    def start_pub(self, client):
        self.should_stop_pub = False
        logging.info('audio start pub')
        self.t2 = threading.Timer(
            self.send_frame, self.publish, args=(client,))
        self.t2.start()

    def publish(self, client):
        logging.debug("audio buffer:" + str(len(self.buffer)))
        if self.buffer != []:
            logging.debug('audio pubing')
            data = self.buffer.pop(0)
            client.publish(topic='/IoT/audio', payload=data)
            logging.debug('audio pubbed')
        if not self.should_stop_pub:
            self.t2 = threading.Timer(
                self.send_frame, self.publish, args=(client,))
            self.t2.start()

    def stop_pub(self):
        logging.info('audio stop pub')
        self.should_stop_pub = True
        self.t2.cancel()


class IotDevice(object):
    def __init__(self):
        self.video = Video()
        self.audio = Audio()

    def on_connect(self, client, userdata, flags, rc):
        logging.info('connected')
        topic = "/IoT/ctrl"
        mqttc.subscribe(topic, 2)
        return

    def on_publish(self):
        return

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info("subscribed")
        return

    def on_message(self, client, userdata, message):
        # message:[topic, payload, qos, retain]
        if message.topic == "/IoT/ctrl":
            data = json.loads(str(bytes(message.payload), "utf-8"))
            logging.info(data)
            if data['type'] == 'ctrl':
                if data['dev_type'] == 'video':
                    self.on_video(client, data['action'])
                elif data['dev_type'] == 'audio':
                    self.on_audio(client, data['action'])
        return

    def on_video(self, client, action):
        if action == 'on':
            logging.info('video on')
            self.video.start_rec()
            self.video.start_pub(client)
        elif action == 'off':
            self.video.stop_rec()
            self.video.stop_pub()
        return

    def on_audio(self, client, action):
        if action == 'on':
            logging.info('audio on')
            self.audio.start_rec()
            self.audio.start_pub(client)
        elif action == 'off':
            self.audio.stop_rec()
            self.audio.stop_pub()
        return


iot = IotDevice()
mqttc = mqtt.Client()

mqttc.on_connect = iot.on_connect
# mqttc.on_publish = iot.on_publish
mqttc.on_subscribe = iot.on_subscribe
mqttc.on_message = iot.on_message
mqttc.connect("127.0.0.1", port=1883, keepalive=60, bind_address="")
# mqttc.loop_start()
mqttc.loop_forever()