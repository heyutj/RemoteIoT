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

    def start_async(self):
        yield from self.broker.start()

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.start_async())
        asyncio.get_event_loop().run_forever()


class MClient(object):
    def __init__(self, serverAddr="mqtt://127.0.0.1/"):
        self.serverAddr = serverAddr
        self.logger = logging.getLogger(__name__)
        formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=formatter)

    def pub_sub(self, args):
        tasks = [self.pub_sub_coro(p[0], p[1], p[2]) for p in args]
        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

    @asyncio.coroutine
    def pub_sub_coro(self, topic, call_back, atype):
        if atype == "publish":
            try:
                C = MQTTClient()
                ret = yield from C.connect(self.serverAddr)
                while True:
                    tmp=call_back()
                    yield from C.publish(topic, tmp, qos=0x01)
                    self.logger.info(
                        "published " + datetime.now().strftime("%H:%M:%S") + topic)
                yield from C.disconnect()
                self.shouldstop[topic] = False
            except ConnectException as ce:
                self.logger.error("Connection failed: %s" % ce)
                asyncio.get_event_loop().stop()
        elif atype == "subscribe":
            C = MQTTClient()
            yield from C.connect(self.serverAddr)
            yield from C.subscribe([(topic, QOS_2), ])
            self.logger.info("Subscribed")
            try:
                while True:
                    message = yield from C.deliver_message()
                    packet = message.publish_packet
                    call_back(packet.payload.data)
                self.shouldstop[topic] = False
            except ClientException as ce:
                self.logger.error("Client exception: %s" % ce)
        else:
            raise ValueError("Unsupport type: " + atype)
