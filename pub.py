from mqtt_helper import MServer, MClient
from audio_helper import InAudio, OutAudio
from video_helper import InVideo
from iot_device import IotDevice
import asyncio
mc = MClient()
iot = IotDevice(mc)
asyncio.get_event_loop().run_until_complete(iot.run())
asyncio.get_event_loop().run_forever()
