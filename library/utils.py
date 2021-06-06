from gtts import gTTS
import os
import pygame.mixer
from pydub import AudioSegment
from  pydub.playback import play
import json
import speech_recognition as sr
r = sr.Recognizer()

with open("settings.json") as settings_file:
    main_settings = json.load(settings_file)

def say(string):
    tts = gTTS(string)
    tts.save('tts-temp.mp3')
    sound = AudioSegment.from_mp3("tts-temp.mp3")
    sound.export("myfile.wav", format="wav")
    sound = AudioSegment.from_file('myfile.wav')
    sound = sound.set_frame_rate(16000)
    print(string)
    play(sound)

def listen():
    if main_settings['debug_mode'] != True:
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
        try:
                print(r.recognize_google(audio, show_all=True))
                return r.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
    else:
        text = input("What do you want to say? \n :")
        return text
