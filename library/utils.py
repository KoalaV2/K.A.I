from gtts import gTTS
import playsound
import os

def say(string):
    tts = gTTS(string)
    tts.save('tts-temp.mp3')
    playsound.playsound('tts-temp.mp3', True)
    os.remove("tts-temp.mp3")
