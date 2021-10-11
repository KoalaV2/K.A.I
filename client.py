#!/usr/bin/env python3
from gtts import gTTS
from pydub.playback import play
from library import time
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
nodename = main_settings['nodename']

def say(string):
    if main_settings['stfu'] != True:
        tts = gTTS(string)
        tts.save('tts-temp.mp3')
        sound = AudioSegment.from_mp3("tts-temp.mp3")
        sound.export("myfile.wav", format="wav")
        sound = AudioSegment.from_file('myfile.wav')
        sound = sound.set_frame_rate(16000)
        play(sound)
    else:
        print(string)

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

#def adjust():
    #with sr.Microphone() as source:
        #r.adjust_for_ambient_noise(source)
    #return ""

print("Beginning to listen.... \n")

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
                    print("Face recognition disabled, skipping... \n")
                    username = "User"
                greeting = time.greeting
                say(greeting(time.now.hour) + f" {username}, what can I do for you? \n")

                while True:
                    print("Speak now.. \n")
                    inp = listen().lower()

                    if inp in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        say("Returning to standby... Have a great day!")
                        break

                    url = f"http://localhost:5000/?input={inp}&nodename={nodename}"
                    print(f"Request is from node: {nodename}")
                    response = requests.request("GET", url)
                    say(response.text)

                    say("Anything else?")

            except sr.UnknownValueError as err:
                print("Encountered an error: ", err)


if __name__ == "__main__":
    main()
