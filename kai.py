#!/usr/bin/env python3
from library import calculator
from library import time
from library.utils import say
import os
import subprocess
import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    try:
        r.adjust_for_ambient_noise(source)
        print("""Hello user! \n What\'s your name?""")
        say("Hello user! What's your name?")

        name_litsen = r.listen(source)
        name = r.recognize_google(name_litsen)

        say("Welcome " + name)

        print("\n Welcome", name + "\n")
    
        print("What do you want to do today?")
        say("What do you want to do today?")

        command_listen = r.listen(source)
        command = r.recognize_google(command_listen)
        print("You said: " + command + "\n")
        if command in ('open calculator', 'calculator', 'calc'):
            print("Opening calculator now!")
            say("Opening calculator now! Hold on...")
            calculator.calculator()

        elif command in ('show current time','local time', 'current time', 'time'):
            time.time()

        elif command in ('ssh info', 'ssh information'):
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
            say("Goodnight " + name + "Going to sleep now..")
            subprocess.call('systemctl suspend', shell=True)

        else:
            print("Error, something went wrong!")
    except sr.UnknownValueError as err:
        print("Encountered an error: ", err)
