from gtts import gTTS
import os
from  pydub.playback import play
from pydub import AudioSegment

def say(string):

    tts = gTTS(string)
    tts.save('tts-temp.mp3')
    sound = AudioSegment.from_file('tts-temp.mp3')
    sound = sound.set_frame_rate(16000)
    play(sound)
    os.remove("tts-temp.mp3")
