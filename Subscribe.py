import logging
import asyncio
from AudioHelper import OutAudio
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

#
# This sample shows how to subscbribe a topic and receive data from incoming messages
# It subscribes to '$SYS/broker/uptime' topic and displays the first ten values returned
# by the broker.
#

logger = logging.getLogger(__name__)
oa = OutAudio()


@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://127.0.0.1/')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    yield from C.subscribe([
        ('remote/audio', QOS_1),
    ])
    logger.info("Subscribed")
    try:
        while True:
            message = yield from C.deliver_message()
            packet = message.publish_packet
            oa.playFrame(bytes(packet.payload.data))
            # print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        # yield from C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
        # logger.info("UnSubscribed")
        # yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())
