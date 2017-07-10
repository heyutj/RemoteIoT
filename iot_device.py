from mqtt_helper import MClient
from video_helper import InVideo
from audio_helper import InAudio
from timer import Timer
import json
import threading
import time


class IotDevice(object):
    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.topic_list = ['ctrl']
        self.action_buffer = []
        self.video_frame = 0.05
        self.audio_frame = 0.05
        self.timer_dict = {}

    async def run(self):
        await self.mqtt.connect()
        await self.mqtt.subscribe('ctrl')
        await self.on_video(0, "on")
        await self.on_audio(0, "on")
        while True:
            # print("going")
            # if self.action_buffer == []:
            #     payload = await self.mqtt.get_message()
            #     if payload and payload.topic == 'ctrl':
            #         self.on_ctrl(payload.data)
            # else:
            if self.action_buffer != []:
                action = self.action_buffer.pop(0)
                await action[0](action[1])

    def on_ctrl(self, raw_data):
        data = json.dump(raw_data)
        if data['type'] == 'ctrl':
            if data['device_type'] == "video":
                self.on_video(data['device_id'], data['action'])

    def add_action(self, time, action, args):
        if action == "publish":
            self.action_buffer.append(
                [self.mqtt.publish, args])
        self.timer_dict[args[0]] = threading.Timer(
            time, self.add_action, (time, action, args))
        self.timer_dict[args[0]].start()

    async def on_video(self, device_id, action):
        topic = "Iot/Video/" + str(device_id)
        if action == "on":
            self.iv = InVideo(device_id=device_id)
            self.iv.start()
            self.timer_dict[topic] = threading.Timer(self.video_frame, self.add_action, (
                self.video_frame, "publish", (topic, self.iv.get_frame)))
            self.timer_dict[topic].start()
        elif action == "off":
            self.iv.stop()
            self.timer_dict[topic].stop()

    async def on_audio(self, device_id, action):
        topic = "Iot/Audio/" + str(device_id)
        if action == "on":
            self.ia = InAudio(device_id=device_id)
            self.ia.start()
            self.timer_dict[topic] = threading.Timer(self.audio_frame, self.add_action, (
                self.video_frame, "publish", (topic, self.ia.get_frame)))
            self.timer_dict[topic].start()
        elif action == "off":
            self.ia.stop()
            self.timer_dict[topic].stop()