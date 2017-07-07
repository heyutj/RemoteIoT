from mqtt_helper import MServer, MClient
from audio_helper import InAudio, OutAudio
import asyncio

ms = MServer()
asyncio.get_event_loop().run_until_complete(ms.start())
asyncio.get_event_loop().run_forever()