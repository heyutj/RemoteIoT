from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import *
from hbmqtt.broker import Broker
import asyncio
import os


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
                }
            }
        else:
            self.config = user_config
        self.broker = Broker(self.config)

    async def start(self):
        await self.broker.start()


class MClient(object):
    def __init__(self, serverAddr="mqtt://127.0.0.1/"):

        self.serverAddr = serverAddr
        self.C = MQTTClient()

    async def connect(self):
        try:
            ret = await self.C.connect(self.serverAddr)
        except ConnectException as ce:
            print("Connection failed: %s" % ce)

    async def subscribe(self, topic):
        await self.C.subscribe([(topic, QOS_2), ])

    async def get_message(self):
        message = await self.C.deliver_message()
        return message.publish_packet

    async def publish(self, args):
        tmp = args[1]()
        if tmp==None:
            return
        # print("publishing"+args[0])
        await self.C.publish(args[0], tmp, qos=0x02)
        # print("published")
