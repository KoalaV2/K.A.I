#!/usr/bin/env python3
from gtts import gTTS
from pydub.playback import play
from library.utils import say
from library import calculator
from library import time
import library.youtube_dl as youtube
from library import wikipedia_summary
from library import weather
from library import light
from library import google_query
import library.face as face_rec
import os
import subprocess
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import re
import json
import requests

r = sr.Recognizer()
with open("settings.json") as settings_file:
    main_settings = json.load(settings_file)

trigger = main_settings['trigger']
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

def adjust():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    return ""

print("Beginning to listen....")
adjust()

def main():
    while 1:
        if listen() == trigger:
            try:
                #sound = AudioSegment.from_mp3('library/sounds/wake_up_noise.mp3')
                #play(sound)
                if main_settings["face_rec_toggle"] == True:
                    print("identifying face....")
                    face_rec.face_rec()
                    username = face_rec.global_name
                else:
                    print("Face recognition disabled, skipping...")
                    username = "User"
                greeting = time.greeting
                say(greeting(time.now.hour) + f" {username}, what can I do for you?")

                while True:
                    print("Speak now..")
                    inp = listen().lower()

                    if inp in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        say("Returning to standby... Have a great day!")
                        break

                    url = f"http://localhost:5000/?input={inp}"
                    response = requests.request("GET", url)
                    say(response.text)

                    say("Anything else?")

            except sr.UnknownValueError as err:
                print("Encountered an error: ", err)


if __name__ == "__main__":
    main()
