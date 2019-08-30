#!/usr/bin/env python3
import library.calculator as calculator
import library.time as time
import os
import subprocess
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
r = sr.Recognizer()
engine.setProperty('rate', 160)
with sr.Microphone() as source:
    try:
        r.adjust_for_ambient_noise(source)
        print("""Hello user! \n What\'s your name?""")
        engine.say("Hello user! What's your name?")
        engine.runAndWait()
        name_litsen = r.listen(source)
        name = r.recognize_google(name_litsen)

        engine.say("Welcome " + name)
        engine.runAndWait()
        print("\n Welcome", name + "\n")
    
        print("What do you want to do today?")
        engine.say("What do you want to do today?")
        engine.runAndWait()
        command_listen = r.listen(source)
        command = r.recognize_google(command_listen)
        print("You said: " + command + "\n")
        if command in ('open calculator', 'calculator', 'calc'):
            print("Opening calculator now!")
            engine.say("Opening calculator now! Hold on...")
            calculator.calculator()

        elif command in ('show current time','local time', 'current time', 'time'):
            time.time()

        elif command in ('ssh info', 'ssh information'):
            subprocess.call("library/ssh.sh")

        elif command in ('text', 'journal','write to text file'):
            print("What do you want to write to the file? \n")
            engine.say("What do you want to write to the file?")
            engine.runAndWait()
            text_listen = r.listen(source)
            text = r.recognize_google(text_listen)

            text_file = open('text_file.txt', 'w')
            text_file.write(text)

            print("The following has been written to the file: \n \n" + text)
            engine.say("The following has been written to the file" + text)
            engine.runAndWait()
        else:
            print("Error, something went wrong!")
    except sr.UnknownValueError as err:
        print("Encountered an error: ", err)
