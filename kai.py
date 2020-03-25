#!/usr/bin/env python3
from library import calculator
from library import time
from library.utils import say
import library.youtube_dl as youtube
from library import wikipedia_summary
import os
import subprocess
from gtts import gTTS
import playsound
import speech_recognition as sr

r = sr.Recognizer()

trigger = "wake up"
r = sr.Recognizer()

print("Beginning to listen...")

def listen():
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
        try:
                return r.recognize_google(audio)
        except sr.UnknownValueError:
                print("Could not understand audio")
        return ""

while 1:
    if listen() == trigger:
        try:
            print("What do you want me to do?")
            say("What do you want me to do?")
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
                        time.time()

                    elif command in ('SSH info', 'SSH information'):
                        subprocess.call("library/ssh.sh")

                    elif command in ('text', 'journal','write to text file'):
                        print("What do you want to write to the file? \n")
                        say("What do you want to write to the file?")
                        text_listen = r.listen(source)
                        text = r.recognize_google(text_listen)

                        text_file = open('text_file.txt', 'w')
                        text_file.write(text)

                        print("The following has been written to the file: \n \n" + text)
                        say("The following has been written to the file" + text)
                        
                    elif command in ('goodnight', "good night", "night"):
                        say("Goodnight " + "Going to sleep now..")
                        subprocess.call('systemctl suspend', shell=True)

                    elif command in ('download YouTube video', 'get YouTube video', 'download YouTube videos', 'download a YouTube video'):
                        youtube.youtube()
                        
                    elif command in ('find Wikipedia summary', 'find a Wikipedia summary','search Wikipedia summary', 'find Wikipedia summary', 'search Wikipedia for summary'):
                        wikipedia_summary.wikipedia_summary()

                    elif command in ('help', 'show commands', 'show help'):
                        print("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")
                        say("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")

                    elif command in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        print("Exiting program... Have a great day!")
                        say("Exiting program... Have a great day!")
                        break
                    else:
                        print("Error, something went wrong!")
                        say("Error, something went wrong!")
                    say("Anything else?")
                    print("Anything else?")

        except sr.UnknownValueError as err:
            print("Encountered an error: ", err)
