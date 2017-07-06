from mqtt_helper import MServer, MClient
from audio_helper import InAudio, OutAudio
from video_helper import InVideo
mc = MClient()

iv = InVideo(show_video=True)

mc.publish(['remote/video', iv.get_frame])
