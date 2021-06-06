#!/usr/bin/env python3
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import random
import json
import pickle
import tensorflow
import tflearn
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

r = sr.Recognizer()

def listen():
    if main_settings['debug_mode'] != True:
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
        try:
                print(r.recognize_google(audio, show_all=True))
                return r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return ""
    else:
        text = input("What do you want to say? \n :")
        return text.lower()
def adjust():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    return ""

print("Beginning to listen....")
adjust()


@app.route('/')
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
                    #adjust()
                    print("Speak now..")
                    #inp_listen = r.listen(source)
                    #inp = r.recognize_google(inp_listen)
                    inp = listen()
                    results = model.predict([bag_of_words(inp,words)])
                    results_index = numpy.argmax(results)
                    tag = labels[results_index]
                    for tg in data["intents"]:
                        if tg['tag'] == tag:
                            responses = tg['responses']
                    resp = random.choice(responses)
                    print("You said: " + inp + "\n")
                    if inp.find("calculator") != -1:
                        say("Opening calculator now!")
                        calculator.calculator()

                    elif inp.find('SSH') != -1:
                        subprocess.call("library/ssh.sh")

                    elif inp in ('text', 'write to a text file', 'Journal','write to text file'):
                        say("What do you want to write to the file? \n")
                        text_listen = r.listen(source)
                        text = r.recognize_google(text_listen)

                        text_file = open(f'{username}_text_file.txt', 'w')
                        text_file.write(text)

                        say("The following has been written to the file: \n \n" + text)

                    elif inp.startswith('download') and inp.endswith('from youtube'):
                        words2 = inp.split()
                        title = words2[1:][:-2]
                        youtube.youtube(title)

                    elif inp.startswith('find summary about') and inp.endswith('on wikipedia'):
                        words2 = inp.split()
                        summary = words2[3:][:-2]
                        wikipedia_summary.wikipedia_summary(summary)

                    elif inp.find('help') != -1:
                        say("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")

                    elif inp.find('weather') != -1:
                        print(inp.find('weather'))
                        words2 = inp.split()
                        city_name = words2[-1]
                        weather.weather(city_name)

                    elif inp.find('lights') != -1 or inp.find('light') != -1:
                        color2  = inp.split()
                        color = str(color2[-1])
                        light.setlightcolor(color)
                        say("Set the light to " + color)

                    elif inp.find('google') != -1:
                        output = re.search('((?<=search\sfor\s)|(what)|(where)|(who)|(when)|(why)|(which)|(whose)|(how)|(is)|(can))(\w*.)*',inp).group(0)
                        print(f"Doing a google search for {output}")
                        response = google_query.google_search(output)
                        title = response[0]['title']
                        text = response[0]['text']
                        say(title)
                        say(text)

                    elif inp in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        say("Returning to standby... Have a great day!")
                        #shutdown_sound = AudioSegment.from_mp3('library/sounds/shutdown.mp3')
                        #play(shutdown_sound)
                        break
                    else:
                        say(resp)
                    say("Anything else?")
            except sr.UnknownValueError as err:
                print("Encountered an error: ", err)


if __name__ == "__main__":
    app.run(debug=True)
