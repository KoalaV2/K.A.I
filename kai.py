#!/usr/bin/env python3
from library import calculator
from library import time
from library.utils import say
import library.youtube_dl as youtube
from library import wikipedia_summary
from library import weather
import library.face as face_rec
import os
import subprocess
from gtts import gTTS
import playsound
import speech_recognition as sr
import playsound
import library.time
trigger = "wake up"
r = sr.Recognizer()


#say("Beginning to listen")
print("Beginning to listen...")

def listen():
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
        try:
                return r.recognize_google(audio)
        except sr.UnknownValueError:
            return ""

while 1:
    if listen() == trigger or input() == trigger:
        try:
            playsound.playsound('library/sounds/wake_up_noise.wav', True)
            print("identifying face....")
            face_rec.face_rec()
            username = face_rec.global_name
            greeting = time.greeting
            print(greeting(time.now.hour), f" {username}, what can I do for you?")
            say(greeting(time.now.hour) + f" {username}, what can I do for you?")
            while True:
                with sr.Microphone() as source:
                    command_listen = r.listen(source)
                    command = r.recognize_google(command_listen)
                    print("You said: " + command + "\n")
                    if command in ('open calculator', 'calculator', 'calc'):
                        print("Opening calculator now!")
                        say("Opening calculator now!")
                        calculator.calculator()

                    elif command in ('show current time','local time', 'current time', 'time'):
                        print(time.now.hour)

                    elif command in ('SSH info', 'SSH information'):
                        subprocess.call("library/ssh.sh")

                    elif command in ('text', 'write to a text file', 'Journal','write to text file'):
                        print("What do you want to write to the file? \n")
                        say("What do you want to write to the file?")
                        text_listen = r.listen(source)
                        text = r.recognize_google(text_listen)

                        text_file = open(f'{username}_text_file.txt', 'w')
                        text_file.write(text)

                        print("The following has been written to the file: \n \n" + text)
                        say("The following has been written to the file" + text)
                        
                    elif command in ('goodnight', "good night", "night"):
                        say("Goodnight " + "Going to sleep now..")
                        subprocess.call('systemctl suspend', shell=True)

                    elif command.startswith('download') and command.endswith('from YouTube'):
                        words = command.split() 
                        title = words[1:][:-2]
                        youtube.youtube(title)
                        
                    elif command.startswith('find summary about') and command.endswith('on Wikipedia'):
                        words = command.split()
                        summary = words[3:][:-2]
                        wikipedia_summary.wikipedia_summary(summary)

                    elif command in ('help', 'show commands', 'show help'):
                        print("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")
                        say("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")

                    elif command.startswith('look up weather in'):
                        words = command.split()
                        city_name = words[4:]
                        weather.weather(city_name)
                        
                    elif command in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        print("Returning to standby... Have a great day!")
                        say("Returning to standby... Have a great day!")
                        playsound.playsound('library/sounds/shutdown.mp3', True)
                        r.adjust_for_ambient_noise(source)
                        break
                    else:
                        print("Error, something went wrong!")
                        say("Error, something went wrong!")
                    say("Anything else?")
                    print("Anything else?")
                    

        except sr.UnknownValueError as err:
            print("Encountered an error: ", err)
            say("Encountered an error: please wake me up again")
