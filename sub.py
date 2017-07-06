from mqtt_helper import MClient
from audio_helper import OutAudio
from video_helper import OutVideo
mc = MClient()
ov=OutVideo()
mc.subscribe(['remote/video', ov.play_frame])
