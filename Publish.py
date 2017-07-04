import logging
import asyncio
from AudioHelper import InAudio
from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import *
from datetime import datetime


#
# This sample shows how to publish messages to broker using different QOS
# Debug outputs shows the message flows
#

logger = logging.getLogger(__name__)
ia = InAudio()
config = {
    'will': {
        'topic': '/will/client',
        'message': b'Dead or alive',
        'qos': 0x01,
        'retain': True
    }
}


@asyncio.coroutine
def test_coro():
    while True:
        try:
            C = MQTTClient()
            ret = yield from C.connect('mqtt://127.0.0.1/')
            message = yield from C.publish('remote/audio', ia.getFrame(), qos=0x01)
            # message = yield from C.publish('remote/audio', b'2 TEST MESSAGE WITH QOS_0', qos=0x00)
            # print(message)
            logger.info("messages published "+datetime.now().strftime("%H:%M:%S"))
            yield from C.disconnect()
        except ConnectException as ce:
            logger.error("Connection failed: %s" % ce)
            asyncio.get_event_loop().stop()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    formatter = "%(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
