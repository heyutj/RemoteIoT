from mqtt_helper import MClient
from audio_helper import OutAudio


mc2 = MClient()
oa = OutAudio()
mc2.subscribe('remote/audio', oa.playFrame)
