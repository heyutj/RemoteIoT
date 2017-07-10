from mqtt_helper import MClient
import asyncio
import json


class Test(object):
    def __init__(self, mqtt):
        self.mqtt = mqtt

    async def run(self):
        await self.mqtt.connect()
        while True:
            data = input()
            await self.mqtt.publish(('ctrl', bytes(data,"utf-8"), True))


mc = MClient()
t = Test(mc)
asyncio.get_event_loop().run_until_complete(t.run())
asyncio.get_event_loop().run_forever()
