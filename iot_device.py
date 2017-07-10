from mqtt_helper import MClient
from video_helper import InVideo
from audio_helper import InAudio
import json
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG)

class IotDevice(object):
    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.topic_list = ['ctrl']
        self.action_buffer = []
        # [function_name,args]
        self.video_frame = 0.04
        self.audio_frame = 0.05
        self.timer_dict = {}

    async def run(self):
        await self.mqtt.connect()
        await self.mqtt.subscribe('ctrl')
        logging.debug("init getmsg")
        th = threading.Thread(target=self.get_message)
        th.start()
        logging.debug("initted getmsg")
        # self.on_video("on")
        while True:
            # print("send_buffer:"+str(len(self.action_buffer)))
            if self.action_buffer == []:
                None
                # msg = await self.mqtt.get_message()
                # payload = msg.publish_packet
                # if payload and msg.topic == 'ctrl':
                #     self.on_ctrl(payload.data)
            else:
                action = self.action_buffer.pop(0)
                await action[0](action[1])
    async def get_message(self):
        while True:
            logging.info("message received")
            msg=await self.mqtt.get_message()
            self.action_buffer.append([self.on_ctrl,msg])
    def on_ctrl(self, raw_data):
        tmp=str(bytes(raw_data),"utf-8")
        data = json.loads(tmp)
        if data['type'] == 'ctrl':
            if data['device_type'] == "video":
                self.on_video(data['action'])
            elif data['device_type'] == "audio":
                self.on_audio(data['action'])

    def add_action(self, time, action, args):
        if action == "publish":
            self.action_buffer.append(
                [self.mqtt.publish, args])
        self.timer_dict[args[0]] = threading.Timer(
            time, self.add_action, (time, action, args))
        self.timer_dict[args[0]].start()

    def on_video(self, action):
        topic = "Iot/Video/"
        if action == "high":
            self.video_frame *= 1.1
        elif action == "low":
            self.video_frame *= 0.9
        elif action == "reset":
            self.video_frame = 0.04
        elif action == "on":
            self.iv = InVideo()
            self.iv.start()
            self.timer_dict[topic] = threading.Timer(self.video_frame, self.add_action, (
                self.video_frame, "publish", (topic, self.iv.get_frame, False)))
            self.timer_dict[topic].start()
            print(topic + " started")
        elif action == "off":
            self.iv.stop()
            self.timer_dict[topic].cancel()
            print(topic + " stopped")

    def on_audio(self, action):
        topic = "Iot/Audio/"
        if action == "high":
            self.video_frame *= 1.1
        elif action == "low":
            self.video_frame *= 0.9
        elif action == "reset":
            self.video_frame = 0.25
        elif action == "on":

            self.ia = InAudio()
            self.ia.start()
            self.timer_dict[topic] = threading.Timer(self.audio_frame, self.add_action, (
                self.video_frame, "publish", (topic, self.ia.get_frame, False)))
            self.timer_dict[topic].start()
            print(topic + " started")

        elif action == "off":
            self.ia.stop()
            self.timer_dict[topic].cancel()
            print(topic + " stopped")


