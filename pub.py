from mqtt_helper import MClient
from audio_helper import InAudio


mc1 = MClient()
ia = InAudio()
mc1.public('remote/audio', ia.getFrame)
