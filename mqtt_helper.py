import logging
import asyncio
from audio_helper import InAudio
from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import *
from datetime import datetime
import os
import numpy as np
from hbmqtt.broker import Broker
import time


class MServer(object):
    def __init__(self, user_config=None):
        if user_config == None:
            self.config = {
                'listeners': {
                    'default': {
                        'type': 'tcp',
                        'bind': '0.0.0.0:1883',
                    },
                    'ws-mqtt': {
                        'bind': '127.0.0.1:8080',
                        'type': 'ws',
                        'max_connections': 10,
                    },
                },
                # 'sys_interval': 10,
                # 'auth': {
                #     'allow-anonymous': True,
                #     'password-file': os.path.join(os.path.dirname(os.path.realpath(__file__)), "passwd"),
                #     'plugins': [
                #         'auth_file', 'auth_anonymous'
                #     ]

                # }
            }
        else:
            self.config = user_config
        self.broker = Broker(self.config)
        formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
        logging.basicConfig(level=logging.INFO, format=formatter)

    async def start_async(self):
        await self.broker.start()

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.start_async())
        asyncio.get_event_loop().run_forever()


class MClient(object):
    def __init__(self, serverAddr="mqtt://127.0.0.1/"):
        self.serverAddr = serverAddr
        self.logger = logging.getLogger(__name__)
        formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.publish_list=[]
        self.subscribe_list=[]

    def publish(self, args):
        asyncio.get_event_loop().run_until_complete(
            self.publish_async(args[0], args[1]))

    def subscribe(self, args):
        asyncio.get_event_loop().run_until_complete(
            self.subscribe_async(args[0], args[1]))

    async def publish_async(self, topic, call_back):
        if topic in self.publish_list:
            raise ValueError("Already exists: "+topic)
        else:
            self.publish_list.append(topic)
            try:
                C = MQTTClient()
                ret = await C.connect(self.serverAddr)
                while True:
                    tmp = call_back()
                    await C.publish(topic, tmp, qos=0x02)
                    self.logger.info(
                        "published " + datetime.now().strftime("%H:%M:%S") + topic)
                await C.disconnect()
            except ConnectException as ce:
                self.logger.error("Connection failed: %s" % ce)
                asyncio.get_event_loop().stop()

    async def subscribe_async(self, topic, call_back):
        if topic in self.subscribe_list:
            raise ValueError("Already exists: "+topic)
        else:
            self.subscribe_list.append(topic)
            C = MQTTClient()
            await C.connect(self.serverAddr)
            await C.subscribe([(topic, QOS_2), ])
            self.logger.info("Subscribed")
            try:
                while True:
                    message = await C.deliver_message()
                    packet = message.publish_packet
                    call_back(packet.payload.data)
            except ClientException as ce:
                self.logger.error("Client exception: %s" % ce)
