#!/usr/bin/env python3
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import random
import json
import pickle
from gtts import gTTS
from pydub.playback import play
from library.utils import say
from library import calculator
from library import time
import library.youtube_dl as youtube
from library import wikipedia_summary
from library import weather
from library import train
from library.train import bag_of_words
from library.light import setlightcolor
import library.face as face_rec
import os
import subprocess
import speech_recognition as sr
import library.time
from pydub import AudioSegment
from pydub.playback import play
trigger = "hey assistant"
r = sr.Recognizer()

def listen():
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
        try:
                print(r.recognize_google(audio, show_all=True))
                return r.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
def adjust():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    return ""

print("Beginning to listen....")

while 1:
    if listen() == trigger:
        try:
            #sound = AudioSegment.from_mp3('library/sounds/wake_up_noise.mp3')
            #play(sound)
            print("identifying face....")
            face_rec.face_rec()
            username = face_rec.global_name
            greeting = time.greeting
            print(greeting(time.now.hour), f"{username}, what can I do for you?")
            say(greeting(time.now.hour) + f"{username} what can I do for you?")
            while True:
                adjust()
                print("Speak now..")
                with sr.Microphone() as source:
                    inp_listen = r.listen(source)
                    inp = r.recognize_google(inp_listen)
                    trained_model = train.trainmodel(inp)
                    results = trained_model[0]
                    labels = trained_model[1]
                    data = trained_model[2]
                    results_index = numpy.argmax(results)
                    tag = labels[results_index]
                    for tg in data["intents"]:
                        if tg['tag'] == tag:
                            responses = tg['responses']
                    resp = random.choice(responses)
                    print("You said: " + inp + "\n")
                    if inp in ('open calculator', 'calculator', 'calc'):
                        print("Opening calculator now!")
                        say("Opening calculator now!")
                        calculator.calculator()

                    elif inp in ('show current time','local time', 'current time', 'time'):
                        print(time.now.hour)

                    elif inp in ('SSH info', 'SSH information'):
                        subprocess.call("library/ssh.sh")

                    elif inp in ('text', 'write to a text file', 'Journal','write to text file'):
                        print("What do you want to write to the file? \n")
                        say("What do you want to write to the file?")
                        text_listen = r.listen(source)
                        text = r.recognize_google(text_listen)

                        text_file = open(f'{username}_text_file.txt', 'w')
                        text_file.write(text)

                        print("The following has been written to the file: \n \n" + text)
                        say("The following has been written to the file" + text)

                    elif inp.startswith('download') and inp.endswith('from YouTube'):
                        words2 = inp.split()
                        title = words2[1:][:-2]
                        youtube.youtube(title)

                    elif inp.startswith('find summary about') and inp.endswith('on Wikipedia'):
                        words2 = inp.split()
                        summary = words2[3:][:-2]
                        wikipedia_summary.wikipedia_summary(summary)

                    elif inp in ('help', 'show inps', 'show help'):
                        print("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")
                        say("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")

                    elif inp.startswith('look up weather in'):
                        words2 = inp.split()
                        city_name = words2[4:]
                        weather.weather(city_name)
                    elif inp in ('set light','set light color','turn light to'):
                        color2  = inp.split()
                        color = str(color2[-1])
                        print(f"Setting light to {color}")
                        setlightcolor(color)
                        say("Setting light to" + color)

                    elif inp in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        print("Returning to standby... Have a great day!")
                        say("Returning to standby... Have a great day!")
                        #shutdown_sound = AudioSegment.from_mp3('library/sounds/shutdown.mp3')
                        #play(shutdown_sound)
                        r.adjust_for_ambient_noise(source)
                        break
                    else:
                        print(resp)
                        say(resp)
                    say("Anything else?")
                    print("Anything else?")
        except sr.UnknownValueError as err:
            print("Encountered an error: ", err)
