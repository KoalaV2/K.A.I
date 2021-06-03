from gtts import gTTS
import os
import pygame.mixer
from pydub import AudioSegment
from  pydub.playback import play
def say(string):
    tts = gTTS(string)
    tts.save('tts-temp.mp3')
    sound = AudioSegment.from_mp3("tts-temp.mp3")
    sound.export("myfile.wav", format="wav")
    sound = AudioSegment.from_file('myfile.wav')
    sound = sound.set_frame_rate(16000)
    play(sound)
